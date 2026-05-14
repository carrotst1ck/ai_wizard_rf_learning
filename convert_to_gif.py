from moviepy.editor import VideoFileClip

# Load the MP4 video
video_path = "static/style.css - ии маги - Visual Studio Code 2026-05-14 10-18-47.mp4"
clip = VideoFileClip(video_path)

# Convert to GIF
gif_path = "static/battle.gif"
clip.write_gif(gif_path, fps=10)  # Adjust fps as needed for quality/speed

print(f"GIF created at {gif_path}")
