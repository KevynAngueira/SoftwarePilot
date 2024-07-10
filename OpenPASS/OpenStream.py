import os

def play_video(rtsp):
   os.system(f"vlc {rtsp}")


if __name__ == '__main__':
    play_video("rtsp://192.168.53.1:554/live")

    
