ffmpeg -f avfoundation -framerate 30 -video_size 1280x720 -i "0" \
  -c:v libx264 -preset veryfast -tune zerolatency \
  -x264-params "bframes=0:profile=baseline" \
  -pix_fmt yuv420p \
  -f rtsp -rtsp_transport tcp \
  rtsp://test:test@localhost:8554/drsys/test/cam1