import cv2
import numpy as np
import math
import os

def get_dimensions_from_image(image_path):
    if not os.path.exists(image_path):
        print("\n[Error] File not found! Check the path and try again.")
        return None, None

    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        print("\n[Error] Could not find any distinct bloodstain shapes in this image.")
        return None, None
        
    largest_contour = max(contours, key=cv2.contourArea)
    ellipse = cv2.fitEllipse(largest_contour)
    (x, y), (width, length), angle = ellipse
    
    return width, length

# --- INTERACTIVE TERMINAL INTERFACE ---
print("==================================================")
print("     BPA TOOLKIT V3: CRIME SCENE RECONSTRUCTION   ")
print("==================================================")

# 1. Automated Image Scan
image_input = input("\nDrag and drop your bloodstain image here: ").strip().strip("'\"")
w, l = get_dimensions_from_image(image_input)

if w and l:
    print(f"\n[OpenCV Scan Successful]")
    print(f" -> Detected Width:  {round(w, 2)} px")
    print(f" -> Detected Length: {round(l, 2)} px")
    
    # Calculate Impact Angle automatically from scanned dimensions
    sine_value = w / l
    if sine_value <= 1:
        impact_angle = math.degrees(math.asin(sine_value))
        print(f" -> Calculated Impact Angle (α): {round(impact_angle, 2)}°")
        print("--------------------------------------------------")
        
        # 2. 2D Area of Convergence Setup
        print("\n[Step 2: Mapping 2D Area of Convergence]")
        stain_x = float(input("Enter Stain X-coordinate (cm): "))
        stain_y = float(input("Enter Stain Y-coordinate (cm): "))
        
        print("\nLocating convergence point on the floor plane...")
        conv_x = float(input("Enter 2D Convergence Point X-coordinate (cm): "))
        conv_y = float(input("Enter 2D Convergence Point Y-coordinate (cm): "))
        
        # Calculate straight-line horizontal distance on the 2D plane
        distance_to_convergence = math.sqrt((conv_x - stain_x)**2 + (conv_y - stain_y)**2)
        print(f" -> Horizontal Distance to Convergence Point: {round(distance_to_convergence, 2)} cm")
        print("--------------------------------------------------")
        
        # 3. 3D Area of Origin Height
        print("\n[Step 3: Calculating 3D Area of Origin Height]")
        angle_radians = math.radians(impact_angle)
        origin_height_z = math.tan(angle_radians) * distance_to_convergence
        
        # 4. Final Case Summary Display
        print("\n==================================================")
        print("                FINAL CASE RESULTS                ")
        print("==================================================")
        print(f"Stain Location:   ({stain_x}, {stain_y}) cm")
        print(f"Convergence Hub:  ({conv_x}, {conv_y}) cm")
        print(f"Impact Angle:     {round(impact_angle, 2)}°")
        print(f"Calculated Origin Height (Z): {round(origin_height_z, 2)} cm")
        print("==================================================")
        
    else:
        print("\n[Error] Scan anomaly: Calculated width cannot exceed length.")
