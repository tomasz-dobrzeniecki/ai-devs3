import cv2
import numpy as np

def split_image_into_maps(image_path):
    """Split the input image into separate map fragments using horizontal and vertical line detection."""
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")
    # Convert to grayscale and threshold
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)
    height, width = binary.shape
    print(f"Image size: {width}x{height}")
    # Find horizontal lines
    horizontal_lines = [0]  # Start with top edge
    for y in range(height):
        if np.all(binary[y, :] == 255):  # White line
            horizontal_lines.append(y)
    horizontal_lines.append(height)  # Add bottom edge
    # Find vertical lines for each horizontal section
    map_fragments = []
    for i in range(len(horizontal_lines) - 1):
        y1, y2 = horizontal_lines[i], horizontal_lines[i + 1]
        if y2 - y1 < 100:  # Skip small fragments
            continue
        fragment = binary[y1:y2, :]
        if np.mean(fragment) > 250:  # Skip mostly white fragments
            continue
        # Find vertical lines in this section
        vertical_lines = [0]  # Start with left edge
        for x in range(width):
            if np.all(fragment[:, x] == 255):  # White line
                vertical_lines.append(x)
        vertical_lines.append(width)  # Add right edge
        # Create fragments
        for j in range(len(vertical_lines) - 1):
            x1, x2 = vertical_lines[j], vertical_lines[j + 1]
            if x2 - x1 < 100:  # Skip small fragments
                continue
            sub_fragment = fragment[:, x1:x2]
            if np.mean(sub_fragment) > 250:  # Skip mostly white fragments
                continue
            if np.mean(sub_fragment) < 255 * 0.95:  # Keep fragments with text
                map_fragments.append((x1, y1, x2, y2))
    # Sort fragments by position
    map_fragments.sort(key=lambda x: (x[1], x[0]))
    # Save fragments
    fragment_paths = []
    for i, (x1, y1, x2, y2) in enumerate(map_fragments):
        fragment = img[y1:y2, x1:x2]
        fragment_path = f"map_fragment_{i}.jpg"
        cv2.imwrite(fragment_path, fragment)
        fragment_paths.append(fragment_path)
        print(f"Saved fragment {i} (size: {x2-x1}x{y2-y1})")
    print(f"Found {len(fragment_paths)} map fragments")
    return fragment_paths 