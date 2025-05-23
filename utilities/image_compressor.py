import os
import argparse
from PIL import Image
import glob

def compress_image(input_path, output_path=None, quality=85, resize_percent=None, max_width=None, max_height=None, convert_format=None):
    """
    Compresses and/or resizes an image.
    
    Args:
        input_path (str): Path to the input image
        output_path (str): Path to save the compressed image
        quality (int): Compression quality (1-100)
        resize_percent (int): Percentage to resize
        max_width (int): Maximum width
        max_height (int): Maximum height
        convert_format (str): Convert to another format
        
    Returns:
        tuple: (new path, original size, new size)
    """
    try:
        img = Image.open(input_path)
        original_format = img.format
        
        if not output_path:
            dirname = os.path.dirname(input_path)
            filename = os.path.basename(input_path)
            name, ext = os.path.splitext(filename)
            
            if convert_format:
                new_ext = f".{convert_format.lower()}"
            else:
                new_ext = ext
                
            output_path = os.path.join(dirname, f"{name}_compressed{new_ext}")
        
        if resize_percent:
            width, height = img.size
            new_width = int(width * resize_percent / 100)
            new_height = int(height * resize_percent / 100)
            img = img.resize((new_width, new_height), Image.LANCZOS)
        
        if max_width or max_height:
            width, height = img.size
            
            if max_width and max_height:
                width_ratio = max_width / width
                height_ratio = max_height / height
                scale = min(width_ratio, height_ratio)
                
                new_width = int(width * scale)
                new_height = int(height * scale)
                
            elif max_width:
                if width > max_width:
                    ratio = max_width / width
                    new_width = max_width
                    new_height = int(height * ratio)
                else:
                    new_width, new_height = width, height
                    
            else:
                if height > max_height:
                    ratio = max_height / height
                    new_height = max_height
                    new_width = int(width * ratio)
                else:
                    new_width, new_height = width, height
            
            img = img.resize((new_width, new_height), Image.LANCZOS)
        
        original_size = os.path.getsize(input_path)
        save_format = convert_format or original_format
        
        if save_format.upper() == 'JPEG' or save_format.upper() == 'JPG':
            img.save(output_path, save_format, quality=quality, optimize=True)
        elif save_format.upper() == 'PNG':
            img.save(output_path, save_format, optimize=True)
        else:
            img.save(output_path, save_format)
        
        new_size = os.path.getsize(output_path)
        
        return (output_path, original_size, new_size)
        
    except Exception as e:
        print(f"Error processing image {input_path}: {str(e)}")
        return None

def process_directory(input_dir, output_dir=None, quality=85, resize_percent=None, max_width=None, max_height=None, convert_format=None, recursive=False, extensions=('jpg', 'jpeg', 'png')):
    """
    Processes all images in a directory.
    
    Args:
        input_dir (str): Directory with images
        output_dir (str): Directory to save processed images
        quality (int): Compression quality
        resize_percent (int): Percentage to resize
        max_width (int): Maximum width
        max_height (int): Maximum height
        convert_format (str): Convert to another format
        recursive (bool): Process directories recursively
        extensions (tuple): File extensions to process
        
    Returns:
        dict: Processing statistics
    """
    if not os.path.isdir(input_dir):
        print(f"The directory '{input_dir}' does not exist.")
        return None
    
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    stats = {
        'processed': 0,
        'failed': 0,
        'original_size': 0,
        'compressed_size': 0
    }
    
    pattern = os.path.join(input_dir, '**' if recursive else '*')
    
    for ext in extensions:
        search_pattern = f"{pattern}/*.{ext}"
        for img_path in glob.glob(search_pattern, recursive=recursive):
            print(f"Processing: {img_path}")
            
            if output_dir:
                rel_path = os.path.relpath(img_path, input_dir)
                output_path = os.path.join(output_dir, rel_path)
                
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                if convert_format:
                    output_path = os.path.splitext(output_path)[0] + f".{convert_format.lower()}"
            else:
                output_path = None
            
            result = compress_image(
                img_path, output_path, quality, resize_percent,
                max_width, max_height, convert_format
            )
            
            if result:
                out_path, orig_size, new_size = result
                stats['processed'] += 1
                stats['original_size'] += orig_size
                stats['compressed_size'] += new_size
                
                reduction = (1 - new_size / orig_size) * 100
                
                print(f"  Original: {orig_size/1024:.1f} KB")
                print(f"  Compressed: {new_size/1024:.1f} KB")
                print(f"  Reduction: {reduction:.1f}%")
            else:
                stats['failed'] += 1
    
    return stats

def main():
    parser = argparse.ArgumentParser(description='Image Compressor and Resizer')
    parser.add_argument('input', type=str, 
                        help='Path of the image or directory to process')
    parser.add_argument('-o', '--output', type=str,
                        help='Output path (file or directory)')
    parser.add_argument('-q', '--quality', type=int, default=85,
                        help='Compression quality (1-100)')
    parser.add_argument('-r', '--resize', type=int,
                        help='Percentage to resize (e.g., 50 for 50%%)')
    parser.add_argument('-w', '--max-width', type=int,
                        help='Maximum image width in pixels')
    parser.add_argument('-ht', '--max-height', type=int,
                        help='Maximum image height in pixels')
    parser.add_argument('-f', '--format', type=str, choices=['jpg', 'jpeg', 'png', 'webp'],
                        help='Convert to another format')
    parser.add_argument('-R', '--recursive', action='store_true',
                        help='Process directories recursively')
    parser.add_argument('-e', '--extensions', type=str, default='jpg,jpeg,png',
                        help='File extensions to process (comma separated)')
    
    args = parser.parse_args()
    
    print('\n' + '='*60)
    print(' IMAGE COMPRESSOR AND RESIZER ')
    print('='*60)
    
    extensions = [ext.strip().lower() for ext in args.extensions.split(',')]
    
    if os.path.isdir(args.input):
        print(f"Processing directory: {args.input}")
        
        stats = process_directory(
            args.input, args.output, args.quality, args.resize,
            args.max_width, args.max_height, args.format,
            args.recursive, extensions
        )
        
        if stats:
            print("\nProcessing summary:")
            print(f"Images processed: {stats['processed']}")
            print(f"Failed images: {stats['failed']}")
            
            if stats['processed'] > 0:
                total_reduction = (1 - stats['compressed_size'] / stats['original_size']) * 100
                print(f"Total original size: {stats['original_size']/1024/1024:.2f} MB")
                print(f"Total compressed size: {stats['compressed_size']/1024/1024:.2f} MB")
                print(f"Total reduction: {total_reduction:.1f}%")
        
    else:
        print(f"Processing image: {args.input}")
        
        result = compress_image(
            args.input, args.output, args.quality, args.resize,
            args.max_width, args.max_height, args.format
        )
        
        if result:
            out_path, orig_size, new_size = result
            reduction = (1 - new_size / orig_size) * 100
            
            print("\nResult:")
            print(f"Image saved at: {out_path}")
            print(f"Original size: {orig_size/1024:.1f} KB")
            print(f"Compressed size: {new_size/1024:.1f} KB")
            print(f"Reduction: {reduction:.1f}%")
    
    print('='*60 + '\n')

if __name__ == "__main__":
    main()
