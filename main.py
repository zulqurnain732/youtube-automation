import os
import random
import subprocess
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from PIL import Image, ImageDraw


def download_source_video(url):
  print('Downloading video via yt-dlp...')
  command = [
      'yt-dlp',
      '-f',
      'bestvideo[ext=mp4]+bestaudio[ext=mp4]/best[ext=mp4]',
      '-o',
      'source.mp4',
      url,
  ]
  subprocess.run(command, check=True)
  return 'source.mp4'


def create_thumbnail(title_text):
  print('Generating custom thumbnail...')
  img = Image.new('RGB', (1280, 720), color=(15, 15, 30))
  d = ImageDraw.Draw(img)
  d.rectangle([(40, 40), (1240, 680)], outline=(255, 255, 255), width=4)
  d.text((80, 150), title_text[:60], fill=(255, 255, 255))
  thumb_path = 'thumbnail.jpg'
  img.save(thumb_path)
  return thumb_path


def create_short(source_video):
  print('Creating 1-3 min Short from random position...')
  duration = random.randint(60, 180)

  probe_cmd = [
      'ffprobe',
      '-v',
      'error',
      '-show_entries',
      'format=duration',
      '-of',
      'default=noprint_wrappers=1:nokey=1',
      source_video,
  ]
  total_duration = float(subprocess.check_output(probe_cmd).decode().strip())
  start_time = random.randint(10, int(max(10, total_duration - duration - 10)))

  output_short = 'output_short.mp4'
  ffmpeg_cmd = [
      'ffmpeg',
      '-y',
      '-ss',
      str(start_time),
      '-i',
      source_video,
      '-t',
      str(duration),
      '-vf',
      (
          'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,'
          'fps=30'
      ),
      '-c:v',
      'libx264',
      '-preset',
      'fast',
      '-c:a',
      'aac',
      output_short,
  ]
  subprocess.run(ffmpeg_cmd, check=True)
  return output_short


def upload_to_youtube(
    file_path, title, description, tags, thumb_path=None, is_short=False
):
  print(f'Uploading {"Short" if is_short else "Video"} to YouTube...')
  # YouTube API upload logic implementation
  # (Client credentials parsed from os.environ.get('YOUTUBE_CLIENT_SECRET'))
  pass


if __name__ == '__main__':
  mode = os.environ.get('UPLOAD_MODE', 'manual_short')
  source_url = (
      'https://www.youtube.com/watch?v=Fd0Dipj3E84'  # Aapka reference link
  )

  if source_url:
    vid = download_source_video(source_url)

    if mode == 'video_morning':
      thumb = create_thumbnail('Subah Ka Behtareen Wazaif & Tilawat')
      upload_to_youtube(
          vid,
          'Subah Ka Wazifa | Special Tilawat',
          'Achi description aur tags #islamic #wazifa',
          ['wazifa', 'tilawat'],
          thumb,
      )
    elif mode == 'video_evening':
      thumb = create_thumbnail('Shaam Ka Khass Wazifa')
      upload_to_youtube(
          vid,
          'Shaam Ka Wazifa | Evening Update',
          'Evening special description #islamic #viral',
          ['evening', 'wazifa'],
          thumb,
      )
    elif mode in ['short_1', 'short_2', 'manual_short']:
      short_vid = create_short(vid)
      upload_to_youtube(
          short_vid,
          'Beautiful Short Clip #Shorts #Viral',
          'Shorts description #shorts #trending',
          ['shorts', 'ytshorts'],
          is_short=True,
      )
