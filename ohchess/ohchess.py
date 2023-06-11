import json
import chess
import csv

def generate_svg_gallery(image_tree, output_file):
    """
    Generate an HTML file with a slideshow of SVG images and a tree-like connection.

    Args:
        image_tree (dict): A dictionary representing the tree structure of images.
                           Each key is a parent image, and the value is a list of child images.
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
        }}
        .slideshow-image {{
          display: block;
          margin: 0 auto;
          max-width: 100%;
          max-height: 600px;
        }}
        .slideshow-controls {{
          text-align: center;
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
        <a class="prev" onclick="goToSlide('{prev_image}')" style="color: {prev_color}">&#10094;</a>
        <a class="next" onclick="goToSlide('{next_image}')" style="color: {next_color}">&#10095;</a>
      </div>
      <ul class="slideshow-list">
        {image_list}
      </ul>
      <script>
        var currentImage = '{current_image}';
        var imageTree = {image_tree};
        var slides = document.getElementsByClassName("slideshow-image");
        var prevButton = document.getElementsByClassName("prev")[0];
        var nextButton = document.getElementsByClassName("next")[0];
        var imageList = document.getElementsByClassName("slideshow-list")[0].getElementsByTagName("a");
        showSlide(currentImage);

        function showSlide(image) {{
          for (var i = 0; i < slides.length; i++) {{
            slides[i].style.display = "none";
          }}

          document.getElementById(image).style.display = "block";
          currentImage = image;
          updateImageList();
          updateControls();
        }}

        function goToSlide(image) {{
          if (image in imageTree) {{
            showSlide(image);
          }}
        }}

        function updateImageList() {{
          for (var i = 0; i < imageList.length; i++) {{
            var image = imageList[i].getAttribute('data-image');
            if (image === currentImage) {{
              imageList[i].classList.add("current");
            }} else {{
              imageList[i].classList.remove("current");
            }}
          }}
        }}

        function updateControls() {{
          var parentImage = null;
          for (var key in imageTree) {{
            if (imageTree[key].includes(currentImage)) {{
              parentImage = key;
              break;
            }}
          }}

          if (parentImage) {{
            prevButton.style.color = "{prev_color}";
            prevButton.setAttribute('onclick', "goToSlide('" + parentImage + "')");
          }} else {{
            prevButton.style.color = "#ccc";
            prevButton.removeAttribute('onclick');
          }}

          if (currentImage in imageTree) {{
            nextButton.style.color = "{next_color}";
            nextButton.setAttribute('onclick', "goToSlide('" + currentImage + "')");
          }} else {{
            nextButton.style.color = "#ccc";
            nextButton.removeAttribute('onclick');
          }}
        }}

        function generateImageList() {{
          var listHTML = "";
          if (currentImage in imageTree) {{
            for (var i = 0; i < imageTree[currentImage].length; i++) {{
              var image = imageTree[currentImage][i];
              listHTML += '<li><a href="#" onclick="goToSlide(\'' + image + '\')" data-image="' + image + '">' + image.split(".svg")[0] + '</a></li>';
            }}
          }}
          return listHTML;
        }}

        updateImageList();
        updateControls();

        var imageListHTML = generateImageList();
        document.getElementsByClassName("slideshow-list")[0].innerHTML = imageListHTML;
      </script>
    </body>
    </html>
    """

    slideshow_template = """
    <div class="slideshow-container">
      <img id="{image}" class="slideshow-image" src="{image}">
    </div>
    """

    image_list_template = """
    <li><a href="#" onclick="goToSlide('{image}')" data-image="{image}">{image_name}</a></li>
    """

    current_image = list(image_tree.keys())[0]
    slideshow = ""
    image_list_html = ""
    for image in image_tree.keys():
        slideshow += slideshow_template.format(image=image)
        image_name = image.split(".svg")[0]
        image_list_html += image_list_template.format(image=image, image_name=image_name)

    prev_color = "#000" if current_image in image_tree.values() else "#ccc"
    next_color = "#000" if current_image in image_tree.keys() else "#ccc"

    html_content = html_template.format(
        current_image=current_image,
        slideshow=slideshow,
        image_list=image_list_html,
        prev_color=prev_color,
        next_color=next_color,
        prev_image=list(image_tree.keys())[0],
        next_image=image_tree[current_image][0] if current_image in image_tree else "",
        image_tree=json.dumps(image_tree),
    )

    # Write the HTML content to a file
    with open(output_file, "w") as file:
        file.write(html_content)

    print("HTML file generated successfully.")


def read_image_tree_from_json(json_file):
    with open(json_file, "r") as file:
        image_tree_json = json.load(file)
    return image_tree_json



def generate_chess_positions(image_tree):
    positions = {}

    def dfs(start_image):
        print(start_image)
        board = chess.Board()
        stack = [(board, start_image)]

        while stack:
            board, current_image = stack.pop()
            print(current_image)
            current_position = board.fen()

            if current_image not in positions:
                positions[current_image] = current_position

            next_images = image_tree.get(current_image, [])
            for next_image in next_images:
                move = board.parse_san(next_image)
                if board.is_legal(move):
                    new_board = board.copy()
                    new_board.push(move)
                    stack.append((new_board, next_image))

    for start_image in image_tree.keys():
        dfs(start_image)

    return positions

def read_move_list_from_csv(filename):
    move_list = {}

    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        for row in reader:
            if row:
                move = row[0].strip()
                variations = [variation.strip() for variation in row[1:] if variation.strip()]
                move_list[move] = variations

    return move_list