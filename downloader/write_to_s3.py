import subprocess
import time
import m3u8_url

def build_command(m3u8_url, trailer):
  # command = [
  #   "ffmpeg", "-i", f"{m3u8_url}", "-movflags", 
  #   "+frag_keyframe+separate_moof+omit_tfhd_offset+empty_moov", 
  #   "-bsf:a", "aac_adtstoasc",
  #   "-f", "mp4", "-c", "copy", f"{trailer}"
  # ]
  command = [
    "ffmpeg", "-i", m3u8_url, "-c", "copy", "-f", "segment", "-segment_list", "out.list", "%010d.ts"
  ]

  return command

def write_to_s3_segments(m3u8_url, channel_name, timestamp):
  s3_object_name = f"{channel_name}/{timestamp}/%10d.ts"
  log_file_name = f"{s3_object_name}.log"
  s3_uri = "s3://arn:aws:s3:ap-northeast-2:492514981574:accesspoint/upload-from-ec2-test"
  s3_path = f"{s3_uri}/{s3_object_name}"
  command = build_command(m3u8_url, f"pipe:1 | aws s3 cp - {s3_path}")

def write_to_s3(m3u8_url, channel_name, timestamp):
  s3_object_name = f"{channel_name}-{timestamp}.mp4"
  log_file_name = f"{s3_object_name}.log"
  s3_uri = "s3://arn:aws:s3:ap-northeast-2:492514981574:accesspoint/upload-from-ec2-test"
  s3_path = f"{s3_uri}/{s3_object_name}"
  command = build_command(m3u8_url, f"pipe:1 | aws s3 cp - {s3_path}")
  with open(log_file_name, "ab") as out:
    proc = subprocess.Popen(command, shell=False, stdout=out)
    proc.wait()
  return proc.pid

def write_to_file(m3u8_url, channel_name, timestamp):
  output_name = f"{channel_name}-{timestamp}.mp4"
  log_file_name = f"{output_name}.log"
  command = build_command(m3u8_url, output_name)
  with open(log_file_name, "ab") as out:
    proc = subprocess.Popen(command, shell=False, stdout=out)
    proc.wait()
  return proc.id


if __name__ == "__main__":
  channel_name = input("channel name: ")
  is_s3 = input("upload to s3 [T/F]: ")
  url = m3u8_url.get(channel_name)
  if (is_s3 == "T"):
    pid = write_to_s3(url, channel_name, time.time())
  else:
    pid = write_to_file(url, channel_name, time.time())