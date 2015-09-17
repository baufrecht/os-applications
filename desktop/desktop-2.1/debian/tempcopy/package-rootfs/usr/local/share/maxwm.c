#include <X11/Xlib.h>

int main(void) {
	Display *dpy;
	if(!(dpy = XOpenDisplay(0x0))) return 1;
	XEvent ev;
	int scr = DefaultScreen(dpy);
	int sw = DisplayWidth(dpy, scr);
	int sh = DisplayHeight(dpy, scr);
	Window w, root = RootWindow(dpy, scr);
	XSelectInput(dpy, root, SubstructureRedirectMask);
	while (!XNextEvent(dpy, &ev)) {
		if (ev.type == MapRequest && (w=ev.xmaprequest.window)) {
			XMoveResizeWindow(dpy, w, 0, 0, sw, sh);
			XMapWindow(dpy, w);
			XSetInputFocus(dpy, w, RevertToPointerRoot, CurrentTime);
			XFlush(dpy);
		}
	}
	return 0;
}
/* TODO: implement: exec desktop files in HOME/.config/autostart
