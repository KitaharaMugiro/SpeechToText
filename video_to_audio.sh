filename_mp4=Lesson3_20191030
export GOOGLE_APPLICATION_CREDENTIALS=./abceed-app-f959c792ae4b.json
echo filename_mp4
echo $GOOGLE_APPLICATION_CREDENTIALS

ffmpeg -i resources/$filename_mp4.mp4 -ar 16000 resources/$filename_mp4.flac

gsutil cp resources/$filename_mp4.flac gs://abceed-app.appspot.com/resources/$filename_mp4.flac

python3 longrunning.py gs://abceed-app.appspot.com/resources/$filename_mp4.flac 1