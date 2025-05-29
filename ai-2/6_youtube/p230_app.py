import yt_dlp
from pathlib import Path

def get_youtube_video_info(video_url):
    ydl_opts = {
        # 'cookies' :'./cookies.txt',
        'noplaylist': True,
        'qu=et': True,
        'no_warnings': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(video_url, download=False)
            return {
                'id' : video_info.get['id'],
                'title' : video_info.get('title'),
                'upload_date': video_info.get('upload_date'),
                'channel' : video_info.get('channel'),
                'duration' : video_info.get('duration_string'),
            }
    except Exception as e:
        return f'Error: {e}'

def remove_invalid_char_for_filename(input_str):
    invalid_characters = '<>:"/\|?*'

    for char in invalid_characters:
        input_str = input_str.replace(char, '_')

    while input_str.endwith('.'):
        input_str = input_str[:-1]

    return inpu_str

def download_youtube_video(video_url, folder, filename=None):
    _, title, _, _ = get_youtube_video_info(video_url)
    filename_no_exit = remove_invalid_char_for_filename(title)

    if filename == None:
        download_file = f'{filename_no_exit}.mp4'
    else:
        download_file = filename
    
    outumpl_str = f'{folder}/{download_file}'

    download_path = Path(outtmpl_str)

    ydl_opts = {
        'cookies' :'./data/cookies.txt',
        'format': 'best',
        'outtmpl': outtmpl_str,
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(video_url, download=True)
        title = video_info.get('title')
    return title, download_path

video_url = 'https://www.youtube.com/watch?v=pSJrML-TTmI'
download_folder = './data'
title, download_path = download_youtube_video(video_url, download_folder)

print("- 유튜브 제목 : ", title)
print("- 다운로드한 파일명", download_path.name)