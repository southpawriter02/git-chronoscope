from PIL import Image, ImageDraw, ImageFont, ImageColor

class FrameRenderer:
    """
    A class to render a single frame of the time-lapse video.
    """
    def __init__(self, width, height, bg_color="#141618", text_color="#FFFFFF", font_path=None, font_size=15):
        """
        Initializes the FrameRenderer object.

        :param width: The width of the frame in pixels.
        :param height: The height of the frame in pixels.
        :param bg_color: The background color of the frame in hex format.
        :param text_color: The color of the text in hex format.
        :param font_path: Path to a .ttf font file. If None, a default font will be used.
        :param font_size: The size of the font.
        """
        self.width = width
        self.height = height
        self.bg_color = self._hex_to_rgb(bg_color)
        self.text_color = self._hex_to_rgb(text_color)

        try:
            # This will raise an AttributeError if font_path is None
            self.font = ImageFont.truetype(font_path, font_size)
            self.font_header = ImageFont.truetype(font_path, int(font_size * 1.2))
        except (AttributeError, IOError, OSError):
            if font_path:
                print(f"Warning: Font '{font_path}' not found or could not be loaded. Using default font.")
            self.font = ImageFont.load_default()
            self.font_header = self.font

    def _hex_to_rgb(self, hex_color):
        """
        Converts a hex color string to an RGB tuple.
        """
        try:
            return ImageColor.getrgb(hex_color)
        except (ValueError, TypeError):
            print(f"Warning: Invalid color '{hex_color}'. Using default color.")
            # Return a default color (e.g., white for text, black for bg)
            # This is a simple fallback, might need a more robust solution
            if len(hex_color) > 4: # A simple check
                return (255, 255, 255)
            return (0, 0, 0)

    def render_frame(self, commit_info, file_contents):
        """
        Renders a single frame, including commit info and file contents.

        :param commit_info: A dictionary containing the commit metadata.
        :param file_contents: A dictionary mapping file paths to their content.
        :return: A Pillow Image object.
        """
        img = Image.new('RGB', (self.width, self.height), color=self.bg_color)
        draw = ImageDraw.Draw(img)

        x_padding = 30
        y_padding = 20
        line_spacing = 8

        # --- 1. Render Header (Commit Info) ---
        header_height = self._render_commit_info(draw, commit_info, x_padding, y_padding, line_spacing)

        # --- 2. Render Content (File Tree and Code) ---
        content_y_start = header_height
        draw.line([(x_padding, content_y_start), (self.width - x_padding, content_y_start)], fill=self.text_color, width=1)
        content_y_start += y_padding

        self._render_file_content(draw, file_contents, x_padding, content_y_start, y_padding, line_spacing)

        return img

    def _render_commit_info(self, draw, commit_info, x_padding, y_padding, line_spacing):
        """Renders the header part of the frame with commit information."""
        current_y = y_padding

        author_text = f"Author: {commit_info['author_name']} <{commit_info['author_email']}>"
        date_text = f"Date: {commit_info['date'].strftime('%Y-%m-%d %H:%M:%S')}"

        draw.text((x_padding, current_y), author_text, font=self.font, fill=self.text_color)
        text_height = self.font.getbbox(author_text)[3] - self.font.getbbox(author_text)[1]
        current_y += text_height + line_spacing

        draw.text((x_padding, current_y), date_text, font=self.font, fill=self.text_color)
        text_height = self.font.getbbox(date_text)[3] - self.font.getbbox(date_text)[1]
        current_y += text_height + y_padding

        commit_message = f"Commit: {commit_info['hash']} - {commit_info['message'].splitlines()[0]}"
        draw.text((x_padding, current_y), commit_message, font=self.font_header, fill=self.text_color)
        text_height = self.font_header.getbbox(commit_message)[3] - self.font_header.getbbox(commit_message)[1]
        current_y += text_height + y_padding

        return current_y

    def _render_file_content(self, draw, file_contents, x_padding, y_start, y_padding, line_spacing):
        """
        Renders the file content in a single column.
        A more sophisticated version could use multiple columns.
        """
        current_y = y_start
        file_header_font = self.font_header
        code_font = self.font

        # Sort files for consistent order
        sorted_files = sorted(file_contents.keys())

        for file_path in sorted_files:
            content = file_contents[file_path]

            # Draw file path header
            file_header_text = f"--- {file_path} ---"
            draw.text((x_padding, current_y), file_header_text, font=file_header_font, fill=self.text_color)
            text_height = file_header_font.getbbox(file_header_text)[3] - file_header_font.getbbox(file_header_text)[1]
            current_y += text_height + line_spacing

            # Draw file content
            lines = content.splitlines()
            for line in lines:
                # Stop if we run out of vertical space
                if current_y > self.height - y_padding - 15: # 15 is buffer for '...'
                    draw.text((x_padding, current_y), "...", font=code_font, fill=self.text_color)
                    return # Exit the function entirely

                draw.text((x_padding + 10, current_y), line, font=code_font, fill=self.text_color)
                text_height = code_font.getbbox(line)[3] - code_font.getbbox(line)[1]
                current_y += text_height + (line_spacing // 2)

            current_y += y_padding # Space between files
