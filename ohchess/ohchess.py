def generate_svg_gallery(image_list, output_file):
    """
    Generate an HTML file with a slideshow of SVG images.

    Args:
        image_list (list): A list of SVG image filenames.
        output_file (str): The path to the output HTML file.

    Returns:
        None
    """
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
      <title>SVG Image Slideshow</title>
      <style>
        .slideshow-container {{
          text-align: center;
          margin-bottom: 20px;
          position: relative;
        #   height: 800px;
        }}
        .slideshow-image {{
          display: block;
          margin: 0 auto;
          max-width: 100%;
          max-height: 600px;
          vertical-align: middle;
        }}
        .slideshow-controls {{
          text-align: center;
          position: relative;
          margin-top: 10px;
        }}
        .slideshow-controls a {{
          font-size: 24px;
          padding: 10px 20px;
        }}
        .slideshow-list {{
          text-align: center;
          margin-top: 10px;
          list-style-type: none;
          padding: 0;
        }}
        .slideshow-list li {{
          display: inline-block;
          margin: 0 5px;
        }}
        .slideshow-list li a {{
          text-decoration: none;
          color: #000;
          font-weight: bold;
        }}
        .slideshow-list li a.current {{
          color: #f00;
        }}
        .slideshow-list li.disabled {{
          color: #ccc;
          pointer-events: none;
        }}
        .hide {{
          display: none;
        }}
      </style>
    </head>
    <body>
      {slideshow}
      <div class="slideshow-controls">
        <a class="prev" onclick="plusSlides(-1)" style="color: {prev_color}">&#10094;</a>
        <a class="next" onclick="plusSlides(1)" style="color: {next_color}">&#10095;</a>
      </div>
      <ul class="slideshow-list">
        {image_list}
      </ul>
      <script>
        var slideIndex = 0;
        var slides = document.getElementsByClassName("slideshow-image");
        var prevButton = document.getElementsByClassName("prev")[0];
        var nextButton = document.getElementsByClassName("next")[0];
        var imageList = document.getElementsByClassName("slideshow-list")[0].getElementsByTagName("a");
        showSlides(slideIndex);

        function showSlides(n) {{
          slideIndex = n;

          for (var i = 0; i < slides.length; i++) {{
            slides[i].style.display = "none";
          }}

          slides[slideIndex].style.display = "block";

          if (slideIndex === 0) {{
            prevButton.style.color = "#ccc";
          }} else {{
            prevButton.style.color = "{prev_color}";
          }}

          if (slideIndex === slides.length - 1) {{
            nextButton.style.color = "#ccc";
          }} else {{
            nextButton.style.color = "{next_color}";
          }}

          updateImageList();
        }}

        function plusSlides(n) {{
          var newIndex = slideIndex + n;
          if (newIndex >= 0 && newIndex < slides.length) {{
            showSlides(newIndex);
          }}
        }}

        function goToSlide(index) {{
          if (index >= 0 && index < slides.length) {{
            showSlides(index);
          }}
        }}

        function updateImageList() {{
          for (var i = 0; i < imageList.length; i++) {{
            if (i === slideIndex) {{
              imageList[i].classList.add("current");
            }} else {{
              imageList[i].classList.remove("current");
            }}
          }}
        }}

        updateImageList();
      </script>
    </body>
    </html>
    """

    slideshow_template = """
    <div class="slideshow-container">
      <img class="slideshow-image" src="{image}">
    </div>
    """

    image_list_template = """
    <li><a href="#" onclick="goToSlide({index})">{image_name}</a></li>
    """

    slideshow = ""
    image_list_html = ""
    for i, image in enumerate(image_list):
        slideshow += slideshow_template.format(image=image)
        image_name = image.split(".svg")[0]
        image_list_html += image_list_template.format(index=i, image_name=image_name)

    prev_color = "#000" if len(image_list) > 1 else "#ccc"
    next_color = "#000" if len(image_list) > 1 else "#ccc"

    html_content = html_template.format(
        slideshow=slideshow,
        image_list=image_list_html,
        prev_color=prev_color,
        next_color=next_color,
    )

    # Write the HTML content to a file
    with open(output_file, "w") as file:
        file.write(html_content)

    print("HTML file generated successfully.")
