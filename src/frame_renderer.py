from PIL import Image, ImageDraw, ImageFont

class FrameRenderer:
    """
    A class to render a single frame of the time-lapse video.
    """
    def __init__(self, width, height, bg_color=(20, 22, 24), text_color=(255, 255, 255), font_path=None, font_size=15):
        """
        Initializes the FrameRenderer object.

        :param width: The width of the frame in pixels.
        :param height: The height of the frame in pixels.
        :param bg_color: The background color of the frame.
        :param text_color: The color of the text.
        :param font_path: Path to a .ttf font file. If None, a default font will be used.
        :param font_size: The size of the font.
        """
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.text_color = text_color

        try:
            # This will raise an AttributeError if font_path is None
            self.font = ImageFont.truetype(font_path, font_size)
            self.font_header = ImageFont.truetype(font_path, int(font_size * 1.2))
        except (AttributeError, IOError, OSError):
            if font_path:
                print(f"Warning: Font '{font_path}' not found or could not be loaded. Using default font.")
            self.font = ImageFont.load_default()
            self.font_header = self.font

    def render_frame(self, commit_info, file_tree):
        """
        Renders a single frame.

        :param commit_info: A dictionary containing the commit metadata.
        :param file_tree: A list of file paths.
        :return: A Pillow Image object.
        """
        # Create a new image
        img = Image.new('RGB', (self.width, self.height), color=self.bg_color)
        draw = ImageDraw.Draw(img)

        # --- Render Commit Info ---
        x_padding = 20
        y_padding = 20
        line_spacing = 8

        current_y = y_padding

        # Author and Date
        author_text = f"Author: {commit_info['author_name']} <{commit_info['author_email']}>"
        date_text = f"Date: {commit_info['date'].strftime('%Y-%m-%d %H:%M:%S')}"

        draw.text((x_padding, current_y), author_text, font=self.font, fill=self.text_color)
        text_height = self.font.getbbox(author_text)[3] - self.font.getbbox(author_text)[1]
        current_y += text_height + line_spacing

        draw.text((x_padding, current_y), date_text, font=self.font, fill=self.text_color)
        text_height = self.font.getbbox(date_text)[3] - self.font.getbbox(date_text)[1]
        current_y += text_height + y_padding

        # Commit Message
        commit_message = f"Commit: {commit_info['hash']} - {commit_info['message'].splitlines()[0]}"
        draw.text((x_padding, current_y), commit_message, font=self.font_header, fill=self.text_color)
        text_height = self.font_header.getbbox(commit_message)[3] - self.font_header.getbbox(commit_message)[1]
        current_y += text_height + y_padding

        # --- Render File Tree ---
        draw.line([(x_padding, current_y), (self.width - x_padding, current_y)], fill=self.text_color, width=1)
        current_y += y_padding

        for file_path in file_tree:
            draw.text((x_padding, current_y), file_path, font=self.font, fill=self.text_color)
            text_height = self.font.getbbox(file_path)[3] - self.font.getbbox(file_path)[1]
            current_y += text_height + line_spacing
            if current_y > self.height - y_padding:
                # Stop if we run out of space
                draw.text((x_padding, current_y), "...", font=self.font, fill=self.text_color)
                break

        return img
