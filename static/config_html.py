config_html = """
<!doctype html>
<html>
  <head>
    <style>
      .lds-ring,
      .lds-ring div {
        box-sizing: border-box;
      }
      .lds-ring {
        display: inline-block;
        position: relative;
        width: 80px;
        height: 80px;
      }
      .lds-ring div {
        box-sizing: border-box;
        display: block;
        position: absolute;
        width: 64px;
        height: 64px;
        margin: 8px;
        border: 8px solid currentColor;
        border-radius: 50%;
        animation: lds-ring 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
        border-color: currentColor transparent transparent transparent;
      }
      .lds-ring div:nth-child(1) {
        animation-delay: -0.45s;
      }
      .lds-ring div:nth-child(2) {
        animation-delay: -0.3s;
      }
      .lds-ring div:nth-child(3) {
        animation-delay: -0.15s;
      }
      @keyframes lds-ring {
        0% {
          transform: rotate(0deg);
        }
        100% {
          transform: rotate(360deg);
        }
      }
    </style>
    <title>face_recognition_project</title>
    <script>
      const URLS = {
        get_camera_status: "http://127.0.0.1:8000/get_camera_status",
        video_feed: "http://127.0.0.1:8000/video_feed",
        validate_current_user_with_image: "http://127.0.0.1:8000/validate_current_user_with_image",
      };

      function httpGet(url) {
        return fetch(url, {
          method: "GET",
          headers: {
            Accept: "application/json",
          },
        }).then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        });
      }

      function httpPost(url, body) {
        return fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          body: JSON.stringify(body),
        }).then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        });
      }
    </script>
  </head>
  <body>
    <img src="http://127.0.0.1:8000/video_feed" style="position: fixed; bottom: 50px; left: 50px; border: 1px solid; border-radius: 7px; user-select: none; width: 150px" />
    <p id="output"></p>
    <hr />
    <div>
      <button onclick="checkCameraStatus()">בדוק סטטוס מצלמה</button>
    </div>
    <hr />
    <div>
      <input style="border: 1px solid" type="file" id="imageInput" accept="image/png, image/jpeg" />
      <br />
      <img id="preview" style="width: 150px; display: none; border: 1px solid #ccc" />
      <br />
      <button onclick="uploadImage()">בדוק תמונה מול משתמש נוכחי</button>
    </div>
    <script>
      function checkCameraStatus() {
        httpGet(URLS.get_camera_status)
          .then((res) => {
            output = document.getElementById("output");
            output.innerHTML = JSON.stringify(res, null, 2);
          })
          .catch((err) => {
            output.innerHTML = JSON.stringify(err);
            console.error(err);
          });
      }
      // image
      const imageInput = document.getElementById("imageInput");
      const preview = document.getElementById("preview");

      imageInput.addEventListener("change", () => {
        const file = imageInput.files[0];
        if (!file) return;

        const reader = new FileReader();

        reader.onload = () => {
          preview.src = reader.result;
          preview.style.display = "block";
        };

        reader.readAsDataURL(file);
      });
      function uploadImage() {
        const fileInput = document.getElementById("imageInput");
        const file = fileInput.files[0];

        if (!file) {
          alert("נא לבחור תמונה");
          return;
        }

        const reader = new FileReader();

        reader.onload = function () {
          setLoding(true);
          // reader.result = "data:image/png;base64,AAAA..."
          const base64Image = reader.result.split(",")[1]; // remove prefix

          fetch(URLS.validate_current_user_with_image, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              user_base64_image: base64Image,
            }),
          })
            .then(async (response) => {
              setLoding(false);
              output = document.getElementById("output");

              const data = await response.json(); // parse JSON
              if (!response.ok) {
                output.innerHTML = JSON.stringify(data);
                console.error(data);
              } else {
                console.log("Success:", data);
                let html = "";

                if (Array.isArray(data?.body?.images)) {
                  data?.body?.images?.forEach((i) => {
                    html += `<img src="${i}" width="150">`;
                  });
                }
                html += `<p>${JSON.stringify(data)}</p>`;
                output.innerHTML = html;
              }
            })
            .catch((err) => {
              setLoding(false);
              output.innerHTML = JSON.stringify(err);
              console.error(err);
            });
        };

        reader.readAsDataURL(file);
      }
      function setLoding(open) {
        document.getElementById("loading").style.display = open ? "block" : "none";
      }
    </script>
    <div class="lds-ring" id="loading" style="display: none">
      <div></div>
      <div></div>
      <div></div>
      <div></div>
    </div>
  </body>
</html>
"""
