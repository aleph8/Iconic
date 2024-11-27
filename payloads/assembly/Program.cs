using System;
using System.Runtime.InteropServices;

/**
    Author: Aleph
    Description: Just an example DLL to illustrate loading with .NET
*/

namespace Iconic
{
    public class Program
    {
        [DllImport("user32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
        public static extern int MessageBoxW(IntPtr hWnd, string text, string caption, uint type);

        public const uint MB_OK = 0x0;
        public const uint MB_ICONINFORMATION = 0x40;

        public int payload(string lol)
        {
            MessageBoxW(IntPtr.Zero, lol, "Just Another Bait Window", MB_OK | MB_ICONINFORMATION);
            return 1;
        }
    }
}
