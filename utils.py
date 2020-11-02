def get_frame_count(video_cap):
    total = 0
    while True:
        (grabbed, _) = video_cap.read()
        if not grabbed:
            break
        total += 1
    return total

