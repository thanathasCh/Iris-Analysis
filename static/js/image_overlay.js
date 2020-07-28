let inputImage = '#input-image';
let imageFrame = '#image-frame';

$(document).ready(function () {
    $(inputImage).change(function () {
        const input = this;

        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                const image = document.createElement('img');
                image.height = '500';
                image.align = 'middle';
                image.src = e.target.result;
                $(imageFrame).append(image)
            }

            reader.readAsDataURL(input.files[0]);
        }
    })
})