import os
import shutil
import tempfile
import subprocess
import pyblish.api


class ExtractGif(pyblish.api.Extractor):
    label = "Gif"
    families = ["preview"]
    optional = True
    order = pyblish.api.Extractor.order + 0.1

    def process(self, context, instance):
        output_path = instance.data("outputPath")
        if not output_path:
            return self.log.info("No capture available for conversion.")

        self.log.info("Generating gif from %s" % output_path)

        fps = context.data("fps") or 24
        width = context.data("width") or 512

        generate_palette = (
            "ffmpeg -y -i {input} -vf "
            "\"fps={fps},scale={width}:-1:flags=lanczos,palettegen\" "
            "{palette}")

        generate_gif = (
            "ffmpeg -y -i {input} -i {palette} -filter_complex "
            "\"fps={fps},scale={width}:-1:flags=lanczos[x];"
            "[x][1:v]paletteuse\" "
            "{output}")

        # try:
        tempdir = tempfile.mkdtemp()
        palette = os.path.join(tempdir, "palette.png")
        output = output_path.rsplit(".", 1)[0] + "1.mov"
        self.log.info("Outputting to %s" % output)

        # try:
        output_ = subprocess.call(
            generate_palette.format(
                input=output_path,
                fps=fps,
                width=width,
                palette=palette))
        # except subprocess.CalledProcessError:
        #     self.log.warning("Could not generate palette")

        subprocess.call('ffmpeg -i {0} -c:v libx264 -preset slow -vf -crf 28 -y {1}'.format(output_path, output))

        # try:
        output_ = subprocess.call(
            generate_gif.format(
                input=output_path,
                fps=fps,
                width=width,
                palette=palette,
                output=output))

        self.log.info(output_)
        assert os.path.exists(output_)
        # except subprocess.CalledProcessError:
        #     self.log.warning("Could not generate gif")

        # finally:
        #     shutil.rmtree(tempdir)

        self.log.info("Finished successfully")
