from PIL import Image, ImageDraw, ImageFont, ImageColor
import colorsys

class FrameRenderer:
    """
    A class to render a single frame of the time-lapse video.
    """
    def __init__(self, width, height, bg_color="#141618", text_color="#FFFFFF", font_path=None, font_size=15, no_email=False):
        """
        Initializes the FrameRenderer object.

        :param width: The width of the frame in pixels.
        :param height: The height of the frame in pixels.
        :param bg_color: The background color of the frame in hex format.
        :param text_color: The color of the text in hex format.
        :param font_path: Path to a .ttf font file. If None, a default font will be used.
        :param font_size: The size of the font.
        :param no_email: If True, do not display author emails.
        """
        self.width = width
        self.height = height
        self.bg_color = self._hex_to_rgb(bg_color)
        self.text_color = self._hex_to_rgb(text_color)
        self.no_email = no_email
        self.author_color = None  # Will be set per-frame if author highlighting is enabled

        try:
            # This will raise an AttributeError if font_path is None
            self.font = ImageFont.truetype(font_path, font_size)
            self.font_header = ImageFont.truetype(font_path, int(font_size * 1.2))
        except (AttributeError, IOError, OSError):
            if font_path:
                print(f"Warning: Font '{font_path}' not found or could not be loaded. Using default font.")
            self.font = ImageFont.load_default()
            self.font_header = self.font

    @staticmethod
    def generate_author_colors(authors):
        """
        Generate a distinct color for each author using HSL color space.
        
        :param authors: List of author names.
        :return: Dictionary mapping author names to RGB hex color strings.
        """
        author_colors = {}
        num_authors = len(authors)
        
        for i, author in enumerate(sorted(authors)):
            # Distribute hues evenly across the color wheel
            hue = i / max(num_authors, 1)
            # Use high saturation and medium-high lightness for vibrant, readable colors
            saturation = 0.7
            lightness = 0.6
            
            # Convert HSL to RGB
            r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
            # Convert to 0-255 range and format as hex
            hex_color = "#{:02x}{:02x}{:02x}".format(int(r * 255), int(g * 255), int(b * 255))
            author_colors[author] = hex_color
        
        return author_colors

    def set_author_color(self, color):
        """
        Set the author color for the current frame.
        
        :param color: Hex color string or None to disable.
        """
        if color:
            self.author_color = self._hex_to_rgb(color)
        else:
            self.author_color = None

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

    def render_diff_frame(self, commit_info, file_contents, tree_diff, line_changes):
        """
        Renders a frame with diff highlighting.
        
        :param commit_info: A dictionary containing the commit metadata.
        :param file_contents: A dictionary mapping file paths to their content.
        :param tree_diff: Dictionary mapping file paths to status (added/deleted/modified).
        :param line_changes: Dictionary mapping file paths to line change info.
        :return: A Pillow Image object.
        """
        img = Image.new('RGB', (self.width, self.height), color=self.bg_color)
        draw = ImageDraw.Draw(img)
        
        x_padding = 30
        y_padding = 20
        line_spacing = 8
        
        # Diff colors
        added_color = (40, 80, 40)      # Dark green background
        deleted_color = (80, 40, 40)    # Dark red background
        modified_color = (80, 80, 40)   # Dark yellow background
        added_text = (100, 255, 100)    # Bright green text
        deleted_text = (255, 100, 100)  # Bright red text
        modified_text = (255, 255, 100) # Bright yellow text
        
        # --- 1. Render Header (Commit Info) ---
        header_height = self._render_commit_info(draw, commit_info, x_padding, y_padding, line_spacing)
        
        # --- 2. Render Diff Summary ---
        current_y = header_height
        
        added_count = sum(1 for s in tree_diff.values() if s == 'added')
        deleted_count = sum(1 for s in tree_diff.values() if s == 'deleted')
        modified_count = sum(1 for s in tree_diff.values() if s == 'modified')
        
        if added_count or deleted_count or modified_count:
            diff_summary = f"Changes: +{added_count} added, -{deleted_count} deleted, ~{modified_count} modified"
            draw.text((x_padding, current_y), diff_summary, font=self.font, fill=(180, 180, 180))
            text_height = self.font.getbbox(diff_summary)[3] - self.font.getbbox(diff_summary)[1]
            current_y += text_height + line_spacing
        
        # --- 3. Render separator ---
        draw.line([(x_padding, current_y), (self.width - x_padding, current_y)], fill=self.text_color, width=1)
        current_y += y_padding
        
        # --- 4. Render Files with Diff Highlighting ---
        self._render_file_content_with_diff(
            draw, file_contents, tree_diff, line_changes,
            x_padding, current_y, y_padding, line_spacing,
            added_color, deleted_color, modified_color,
            added_text, deleted_text, modified_text
        )
        
        return img
    
    def _render_file_content_with_diff(self, draw, file_contents, tree_diff, line_changes,
                                        x_padding, y_start, y_padding, line_spacing,
                                        added_bg, deleted_bg, modified_bg,
                                        added_text, deleted_text, modified_text):
        """Renders file content with diff highlighting."""
        current_y = y_start
        file_header_font = self.font_header
        code_font = self.font
        
        # Sort files, showing changed files first
        def sort_key(f):
            status = tree_diff.get(f, 'unchanged')
            priority = {'added': 0, 'modified': 1, 'deleted': 2, 'unchanged': 3}
            return (priority.get(status, 4), f)
        
        sorted_files = sorted(file_contents.keys(), key=sort_key)
        
        for file_path in sorted_files:
            content = file_contents[file_path]
            file_status = tree_diff.get(file_path, 'unchanged')
            file_line_changes = line_changes.get(file_path, {})
            
            # Stop if we run out of vertical space
            if current_y > self.height - y_padding - 50:
                draw.text((x_padding, current_y), "...", font=code_font, fill=self.text_color)
                return
            
            # Draw file path header with status indicator
            status_icon = {
                'added': '+ ',
                'deleted': '- ',
                'modified': '~ ',
                'unchanged': '  '
            }.get(file_status, '  ')
            
            header_color = {
                'added': added_text,
                'deleted': deleted_text,
                'modified': modified_text,
                'unchanged': self.text_color
            }.get(file_status, self.text_color)
            
            file_header_text = f"{status_icon}--- {file_path} ---"
            draw.text((x_padding, current_y), file_header_text, font=file_header_font, fill=header_color)
            text_height = file_header_font.getbbox(file_header_text)[3] - file_header_font.getbbox(file_header_text)[1]
            current_y += text_height + line_spacing
            
            # Draw file content with line highlighting
            lines = content.splitlines()
            for line_num, line in enumerate(lines):
                if current_y > self.height - y_padding - 15:
                    draw.text((x_padding, current_y), "...", font=code_font, fill=self.text_color)
                    return
                
                line_status = file_line_changes.get(line_num)
                
                # Draw background highlight for changed lines
                if line_status == 'added':
                    text_bbox = code_font.getbbox(line) if line else (0, 0, 10, 15)
                    draw.rectangle(
                        [(x_padding + 5, current_y - 2), 
                         (self.width - x_padding, current_y + text_bbox[3] - text_bbox[1] + 2)],
                        fill=added_bg
                    )
                    line_color = added_text
                elif line_status == 'modified':
                    text_bbox = code_font.getbbox(line) if line else (0, 0, 10, 15)
                    draw.rectangle(
                        [(x_padding + 5, current_y - 2),
                         (self.width - x_padding, current_y + text_bbox[3] - text_bbox[1] + 2)],
                        fill=modified_bg
                    )
                    line_color = modified_text
                else:
                    line_color = self.text_color
                
                draw.text((x_padding + 10, current_y), line, font=code_font, fill=line_color)
                text_height = code_font.getbbox(line)[3] - code_font.getbbox(line)[1] if line else 15
                current_y += text_height + (line_spacing // 2)
            
            current_y += y_padding


    def _render_commit_info(self, draw, commit_info, x_padding, y_padding, line_spacing):
        """Renders the header part of the frame with commit information."""
        current_y = y_padding

        author_email = "[email protected]" if self.no_email else commit_info['author_email']
        author_text = f"Author: {commit_info['author_name']} <{author_email}>"
        date_text = f"Date: {commit_info['date'].strftime('%Y-%m-%d %H:%M:%S')}"

        # Use author color for the author line if enabled
        author_line_color = self.author_color if self.author_color else self.text_color
        draw.text((x_padding, current_y), author_text, font=self.font, fill=author_line_color)
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

    def render_comparison_frame(self, left_commit, right_commit, left_files, right_files, left_branch="left", right_branch="right"):
        """
        Renders a side-by-side comparison frame for two branches.
        
        :param left_commit: Dictionary with commit info for left branch (can be None).
        :param right_commit: Dictionary with commit info for right branch (can be None).
        :param left_files: Dictionary of file contents for left branch.
        :param right_files: Dictionary of file contents for right branch.
        :param left_branch: Name of the left branch.
        :param right_branch: Name of the right branch.
        :return: A Pillow Image object.
        """
        img = Image.new('RGB', (self.width, self.height), color=self.bg_color)
        draw = ImageDraw.Draw(img)
        
        x_padding = 20
        y_padding = 15
        line_spacing = 6
        
        # Calculate split point
        mid_x = self.width // 2
        separator_width = 2
        
        # Draw vertical separator
        separator_color = (100, 100, 100)
        draw.line([(mid_x, 0), (mid_x, self.height)], fill=separator_color, width=separator_width)
        
        # Render left side
        self._render_comparison_side(
            draw, left_commit, left_files, left_branch,
            x_start=0, x_end=mid_x - separator_width,
            x_padding=x_padding, y_padding=y_padding, line_spacing=line_spacing
        )
        
        # Render right side
        self._render_comparison_side(
            draw, right_commit, right_files, right_branch,
            x_start=mid_x + separator_width, x_end=self.width,
            x_padding=x_padding, y_padding=y_padding, line_spacing=line_spacing
        )
        
        return img
    
    def _render_comparison_side(self, draw, commit_info, file_contents, branch_name, x_start, x_end, x_padding, y_padding, line_spacing):
        """Render one side of the comparison frame."""
        current_y = y_padding
        side_width = x_end - x_start
        x_offset = x_start + x_padding
        
        # Branch header with distinct color
        branch_color = (100, 255, 218)  # Cyan/teal color
        branch_text = f"Branch: {branch_name}"
        draw.text((x_offset, current_y), branch_text, font=self.font_header, fill=branch_color)
        text_height = self.font_header.getbbox(branch_text)[3] - self.font_header.getbbox(branch_text)[1]
        current_y += text_height + line_spacing
        
        # Horizontal separator under branch name
        draw.line([(x_start + 5, current_y), (x_end - 5, current_y)], fill=(60, 60, 60), width=1)
        current_y += y_padding
        
        if commit_info is None:
            # No commit at this point in time
            no_commit_text = "(no commit at this time)"
            draw.text((x_offset, current_y), no_commit_text, font=self.font, fill=(128, 128, 128))
            return
        
        # Commit hash
        hash_text = f"Commit: {commit_info.get('hash', 'unknown')[:7]}"
        draw.text((x_offset, current_y), hash_text, font=self.font, fill=self.text_color)
        text_height = self.font.getbbox(hash_text)[3] - self.font.getbbox(hash_text)[1]
        current_y += text_height + line_spacing
        
        # Author
        author_text = f"Author: {commit_info.get('author_name', 'Unknown')}"
        draw.text((x_offset, current_y), author_text, font=self.font, fill=self.text_color)
        text_height = self.font.getbbox(author_text)[3] - self.font.getbbox(author_text)[1]
        current_y += text_height + line_spacing
        
        # Date
        date = commit_info.get('date')
        if date:
            date_str = date.strftime('%Y-%m-%d %H:%M') if hasattr(date, 'strftime') else str(date)
            date_text = f"Date: {date_str}"
            draw.text((x_offset, current_y), date_text, font=self.font, fill=self.text_color)
            text_height = self.font.getbbox(date_text)[3] - self.font.getbbox(date_text)[1]
            current_y += text_height + line_spacing
        
        # Message (first line only)
        message = commit_info.get('message', '')
        if message:
            msg_text = message.splitlines()[0][:40] + ("..." if len(message.splitlines()[0]) > 40 else "")
            draw.text((x_offset, current_y), msg_text, font=self.font, fill=(180, 180, 180))
            text_height = self.font.getbbox(msg_text)[3] - self.font.getbbox(msg_text)[1]
            current_y += text_height + y_padding
        
        # File list header
        files_header = f"Files ({len(file_contents)}):"
        draw.text((x_offset, current_y), files_header, font=self.font, fill=branch_color)
        text_height = self.font.getbbox(files_header)[3] - self.font.getbbox(files_header)[1]
        current_y += text_height + line_spacing
        
        # File list
        sorted_files = sorted(file_contents.keys())
        max_files = 20  # Limit files shown
        
        for i, file_path in enumerate(sorted_files[:max_files]):
            if current_y > self.height - y_padding - 30:
                remaining = len(sorted_files) - i
                draw.text((x_offset, current_y), f"... and {remaining} more files", font=self.font, fill=(128, 128, 128))
                break
            
            # Truncate long file paths
            display_path = file_path if len(file_path) < 35 else "..." + file_path[-32:]
            draw.text((x_offset + 10, current_y), f"📄 {display_path}", font=self.font, fill=self.text_color)
            text_height = self.font.getbbox(file_path)[3] - self.font.getbbox(file_path)[1]
            current_y += text_height + (line_spacing // 2)
