import streamlit as st
import os
import tempfile
import asyncio
import edge_tts
import moviepy.editor as mp
from PIL import Image, ImageOps

st.set_page_config(
    page_title="Smart AI Video Creator 2.0",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Smart AI Video Creator 2.0")
st.write("अपनी कहानी, फोटो और आवाज़ चुनें। फिर वीडियो बनाएँ।")

# SETTINGS

voice_options = {
    "हिंदी पुरुष": "hi-IN-MadhurNeural",
    "हिंदी महिला": "hi-IN-SwaraNeural"
}

voice_name = st.selectbox(
    "1. वीडियो की आवाज़ चुनें",
    list(voice_options.keys())
)

voice_rate = st.selectbox(
    "2. आवाज़ की गति",
    ["सामान्य", "धीमी", "तेज़"]
)

rate_map = {
    "सामान्य": "+0%",
    "धीमी": "-15%",
    "तेज़": "+15%"
}

video_format = st.selectbox(
    "3. वीडियो का आकार",
    ["YouTube Shorts (9:16)", "YouTube Landscape (16:9)"]
)

animation = st.selectbox(
    "4. फोटो एनिमेशन",
    [
        "धीमा Zoom In",
        "धीमा Zoom Out",
        "बारी-बारी Zoom In और Zoom Out",
        "बिना एनिमेशन"
    ]
)

script = st.text_area(
    "5. अपनी हिंदी कहानी लिखें (हर लाइन में एक दृश्य)",
    height=200,
    placeholder=(
        "एक घने जंगल में सुबह हुई।\n"
        "जंगल में पक्षियों की आवाज़ गूँजने लगी।\n"
        "तभी एक शेर धीरे-धीरे बाहर आया।"
    )
)

uploaded_files = st.file_uploader(
    "6. एक साथ कई फोटो चुनें",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True,
    help="एक साथ कई फोटो चुन सकते हैं।"
)

if uploaded_files:
    st.success(f"कुल {len(uploaded_files)} फोटो चुनी गईं")

    with st.expander("चुनी गई सभी फोटो देखें"):
        cols = st.columns(3)

        for i, file in enumerate(uploaded_files):
            file.seek(0)

            with cols[i % 3]:
                st.image(file, use_container_width=True)
                st.caption(f"फोटो {i + 1}")


# VIDEO HELPERS

def create_tts(text, voice, rate, output_path):
    async def generate():
        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate=rate
        )
        await communicate.save(output_path)

    asyncio.run(generate())


def prepare_image(file, output_path, size):
    file.seek(0)

    with Image.open(file) as original:
        img = ImageOps.exif_transpose(original).convert("RGB")

    target_w, target_h = size
    target_ratio = target_w / target_h
    img_ratio = img.width / img.height

    if img_ratio > target_ratio:
        new_w = int(img.height * target_ratio)
        left = (img.width - new_w) // 2
        img = img.crop((left, 0, left + new_w, img.height))
    else:
        new_h = int(img.width / target_ratio)
        top = (img.height - new_h) // 2
        img = img.crop((0, top, img.width, top + new_h))

    img = img.resize(size, Image.Resampling.LANCZOS)
    img.save(output_path, quality=92)

    return output_path


def animate_image(image_path, duration, size, mode, scene_index):
    clip = mp.ImageClip(image_path).set_duration(duration)

    if mode == "बिना एनिमेशन" or duration <= 0.5:
        return clip

    if mode == "धीमा Zoom In":
        scale = lambda t: 1.0 + 0.08 * (t / duration)

    elif mode == "धीमा Zoom Out":
        scale = lambda t: 1.08 - 0.08 * (t / duration)

    elif mode == "बारी-बारी Zoom In और Zoom Out":
        if scene_index % 2 == 0:
            scale = lambda t: 1.0 + 0.08 * (t / duration)
        else:
            scale = lambda t: 1.08 - 0.08 * (t / duration)

    else:
        return clip

    w, h = size
    animated = clip.resize(scale)

    animated = animated.crop(
        x_center=animated.w / 2,
        y_center=animated.h / 2,
        width=w,
        height=h
    )

    return animated.set_duration(duration)


# CREATE VIDEO

if st.button("🚀 वीडियो बनाएँ", use_container_width=True):

    if not script.strip():
        st.error("पहले अपनी कहानी लिखें।")

    elif not uploaded_files:
        st.error("कम से कम एक फोटो चुनें।")

    else:
        lines = [
            line.strip()
            for line in script.splitlines()
            if line.strip()
        ]

        if not lines:
            st.error("कहानी में कम से कम एक लाइन लिखें।")
            st.stop()

        voice = voice_options[voice_name]
        rate = rate_map[voice_rate]

        if video_format == "YouTube Shorts (9:16)":
            size = (720, 1280)
        else:
            size = (1280, 720)

        progress = st.progress(0)
        status = st.empty()

        try:
            with tempfile.TemporaryDirectory() as temp_dir:

                audio_clips = []
                image_clips = []
                final_audio = None
                final_video = None

                try:
                    for idx, line in enumerate(lines):

                        status.write(
                            f"🎙️ आवाज़ बना रहे हैं: "
                            f"{idx + 1}/{len(lines)}"
                        )

                        audio_path = os.path.join(
                            temp_dir, f"audio_{idx}.mp3"
                        )

                        create_tts(
                            line,
                            voice,
                            rate,
                            audio_path
                        )

                        audio_clip = mp.AudioFileClip(audio_path)
                        audio_clips.append(audio_clip)

                        image_file = uploaded_files[
                            idx % len(uploaded_files)
                        ]

                        image_path = os.path.join(
                            temp_dir, f"image_{idx}.jpg"
                        )

                        prepare_image(
                            image_file,
                            image_path,
                            size
                        )

                        image_clip = animate_image(
                            image_path,
                            audio_clip.duration,
                            size,
                            animation,
                            idx
                        )

                        image_clips.append(image_clip)

                        progress.progress(
                            int((idx + 1) / len(lines) * 70)
                        )

                    status.write("🎬 सभी दृश्य जोड़ रहे हैं...")

                    final_audio = mp.concatenate_audioclips(
                        audio_clips
                    )

                    final_video = mp.concatenate_videoclips(
                        image_clips,
                        method="compose"
                    ).set_audio(final_audio)

                    output_path = os.path.join(
                        temp_dir, "smart_video.mp4"
                    )

                    final_video.write_videofile(
                        output_path,
                        fps=24,
                        codec="libx264",
                        audio_codec="aac",
                        preset="ultrafast",
                        threads=2,
                        logger=None
                    )

                    progress.progress(100)
                    status.success("✅ आपका वीडियो तैयार है!")

                    st.video(output_path)

                    with open(output_path, "rb") as video_file:
                        video_data = video_file.read()

                    st.download_button(
                        "📥 MP4 वीडियो डाउनलोड करें",
                        data=video_data,
                        file_name="smart_ai_video.mp4",
                        mime="video/mp4",
                        use_container_width=True
                    )

                finally:
                    if final_video is not None:
                        final_video.close()

                    if final_audio is not None:
                        final_audio.close()

                    for clip in image_clips:
                        clip.close()

                    for clip in audio_clips:
                        clip.close()

        except Exception as error:
            st.error("वीडियो बनाते समय समस्या आई।")
            st.code(str(error))
            st.info(
                "यह Error कॉपी करके भेजें, ताकि उसे ठीक किया जा सके।"
            )
