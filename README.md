## SuperMouser

An application to easily control your mouse with the keyboard.

### OSX Installation

1) Build the OSX app
   ```shell
   $ pip install pyinstaller
   $ ./build.osx.app.sh
   $ cp -a build/dist/SuperMouser.app /Applications
   ```

2) Open SuperMouser and allow it to control the mouse in OSX
   1) Go to 'System Settings' -> 'Privacy & Security' -> 'Accessibility' and allow SuperMouser

3) Install something like [Hammerspoon](https://www.hammerspoon.org/) and map a global shortcut to start Supermouser.

   Here is a snippet of my config `~/.hammerspoon/init.lua`:
 
   ```lua
    hs.loadSpoon("AppLauncher");

    spoon.AppLauncher.modifiers = {"shift", "ctrl", "alt"}
    spoon.AppLauncher:bindHotkeys({
        M = "SuperMouser",
      }
    )
   ```



<sup><sub>* Icon downloaded from [icon--icons](https://icon-icons.com/users/antonia_again/icon-sets/) created by [antonia_again](https://icon-icons.com/users/antonia_again/icon-sets/)</sup><sub>
