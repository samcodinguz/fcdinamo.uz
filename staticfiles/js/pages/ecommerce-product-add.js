if ("undefined" != typeof Quill) {
  let i = Quill.import("ui/icons"),
    e =
      ((i.bold = '<i class="ti ti-bold fs-lg"></i>'),
      (i.italic = '<i class="ti ti-italic fs-lg"></i>'),
      (i.underline = '<i class="ti ti-underline fs-lg"></i>'),
      (i.strike = '<i class="ti ti-strikethrough fs-lg"></i>'),
      (i.list = '<i class="ti ti-list fs-lg"></i>'),
      (i.bullet = '<i class="ti ti-list-ul fs-lg"></i>'),
      (i.link = '<i class="ti ti-link fs-lg"></i>'),
      (i.image = '<i class="ti ti-photo fs-lg"></i>'),
      (i["code-block"] = '<i class="ti ti-code fs-lg"></i>'),
      (i.background = '<i class="ti ti-background fs-lg"></i>'),
      (i.blockquote = '<i class="ti ti-blockquote fs-lg"></i>'),
      document.getElementById("snow-editor")),
    t =
      (e &&
        new Quill(e, {
          theme: "snow",
          modules: {
            toolbar: [
              [
                "bold",
                "italic",
                "underline",
                "strike",
                "blockquote",
                "code-block",
                { list: "bullet" },
                "link",
                "image",
              ],
            ],
          },
        }),
      document.getElementById("bubble-editor"));
  t && new Quill("#bubble-editor", { theme: "bubble" });
}
class FileUpload {
  constructor() {}

  init() {
    if (typeof Dropzone === "undefined") {
      console.warn("Dropzone is not loaded.");
      return;
    }

    Dropzone.autoDiscover = false;

    let elements = document.querySelectorAll('[data-plugin="dropzone"]');

    elements.forEach((el) => {
      let url = el.getAttribute("action") || "/";
      let previewsContainer = el.dataset.previewsContainer;
      let previewTemplateSelector = el.dataset.uploadPreviewTemplate;
      let existingImage = el.dataset.existingImage;

      let options = {
        url: url,
        acceptedFiles: "image/*",
        maxFiles: 1,
        addRemoveLinks: true,
      };

      if (previewsContainer)
        options.previewsContainer = previewsContainer;

      if (previewTemplateSelector) {
        let template = document.querySelector(previewTemplateSelector);
        if (template) options.previewTemplate = template.innerHTML;
      }

      let dz = new Dropzone(el, options);

      // 🔥 ASOSIY QISM — OLD RASMNI CHIQARISH
      if (existingImage) {
        let mockFile = {
          name: el.dataset.existingName || "Old image",
          size: 123456,
          accepted: true,
        };

        dz.emit("addedfile", mockFile);
        dz.emit("thumbnail", mockFile, existingImage);
        dz.emit("complete", mockFile);
        dz.files.push(mockFile);
      }
    });
  }
}

document.addEventListener("DOMContentLoaded", () => {
  new FileUpload().init();
});
