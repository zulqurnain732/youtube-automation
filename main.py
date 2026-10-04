import os
import random
import subprocess


def download_source_video(url):
  print("Downloading video via yt-dlp using cookies.txt...")
  command = [
      "yt-dlp",
      "--cookies",
      "cookies.txt",
      "-f",
      "bestvideo[ext=mp4]+bestaudio[ext=mp4]/best[ext=mp4]",
      "-o",
      "source.mp4",
      url,
  ]
  subprocess.run(command, check=True)
  return "source.mp4"


def create_short(source_video):
  print("Creating 1-3 min Short from random position...")
  duration = random.randint(60, 180)  # 1 se 3 minute tak

  probe_cmd = [
      "ffprobe",
      "-v",
      "error",
      "-show_entries",
      "format=duration",
      "-of",
      "default=noprint_wrappers=1:nokey=1",
      source_video,
  ]
  total_duration = float(subprocess.check_output(probe_cmd).decode().strip())
  start_time = random.randint(10, int(max(10, total_duration - duration - 10)))

  output_short = "output_short.mp4"
  ffmpeg_cmd = [
      "ffmpeg",
      "-y",
      "-ss",
      str(start_time),
      "-i",
      source_video,
      "-t",
      str(duration),
      "-vf",
      (
          "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
          "fps=30"
      ),
      "-c:v",
      "libx264",
      "-preset",
      "fast",
      "-c:a",
      "aac",
      output_short,
  ]
  subprocess.run(ffmpeg_cmd, check=True)
  return output_short


if __name__ == "__main__":
  mode = os.environ.get("UPLOAD_MODE", "manual_short")
  source_url = "https://www.youtube.com/watch?v=Fd0Dipj3E84"

  if source_url:
    vid = download_source_video(source_url)

    if mode in ["short_1", "short_2", "manual_short"]:
      short_vid = create_short(vid)
      print(f"Short successfully created: {short_vid}")
      # Yahan YouTube API upload function call hoga
    elif mode == "video_morning" or mode == "video_evening":
      print(f"Video mode {mode} executed using source video.")
