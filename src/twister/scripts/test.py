from pynput.keyboard import Key, Listener

def on_press(key):
    print(" ------" + str(key))
    if key.char == ('d'):
        print(1)
    

def on_release(key):
    if key == Key.esc:
        # Stop listener
        return False

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()