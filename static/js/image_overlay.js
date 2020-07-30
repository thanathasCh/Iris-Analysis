let inputImage = '#input-image';
let imageFrame = '#image-frame';
let processBtn = '#process_btn';
let patternPath = '/static/images/eye-pattern.png';


function update(activeAnchor) {
    var group = activeAnchor.getParent();

    var topLeft = group.find('.topLeft')[0];
    var topRight = group.find('.topRight')[0];
    var bottomRight = group.find('.bottomRight')[0];
    var bottomLeft = group.find('.bottomLeft')[0];
    var image = group.find('Image')[0];

    var anchorX = activeAnchor.getX();
    var anchorY = activeAnchor.getY();

    // update anchor positions
    switch (activeAnchor.getName()) {
        case 'topLeft':
            topRight.y(anchorY);
            bottomLeft.x(anchorX);
            break;
        case 'topRight':
            topLeft.y(anchorY);
            bottomRight.x(anchorX);
            break;
        case 'bottomRight':
            bottomLeft.y(anchorY);
            topRight.x(anchorX);
            break;
        case 'bottomLeft':
            bottomRight.y(anchorY);
            topLeft.x(anchorX);
            break;
    }

    image.position(topLeft.position());

    var width = topRight.getX() - topLeft.getX();
    var height = bottomLeft.getY() - topLeft.getY();
    if (width && height) {
        image.width(width);
        image.height(height);
    }
}


function addAnchor(group, x, y, name) {
    var stage = group.getStage();
    var layer = group.getLayer();

    var anchor = new Konva.Circle({
        x: x,
        y: y,
        stroke: '#666',
        fill: '#ddd',
        strokeWidth: 2,
        radius: 8,
        name: name,
        draggable: true,
        dragOnTop: false,
    });

    anchor.on('dragmove', function () {
        update(this);
        layer.draw();
    });
    anchor.on('mousedown touchstart', function () {
        group.draggable(false);
        this.moveToTop();
    });
    anchor.on('dragend', function () {
        group.draggable(true);
        layer.draw();
    });
    // add hover styling
    anchor.on('mouseover', function () {
        var layer = this.getLayer();
        document.body.style.cursor = 'pointer';
        this.strokeWidth(4);
        layer.draw();
    });
    anchor.on('mouseout', function () {
        var layer = this.getLayer();
        document.body.style.cursor = 'default';
        this.strokeWidth(2);
        layer.draw();
    });

    group.add(anchor);
}


function drawCanvas(imageSrc, size) {
    var width = size.width;
    var height = size.height;


    var stage = new Konva.Stage({
        container: 'image-frame',
        width: width,
        height: height,
    });

    var layer = new Konva.Layer();
    stage.add(layer);

    var imageObj = new Image();
    imageObj.onload = function () {
        var userImage = new Konva.Image({
            image: imageObj,
            height: height,
            width: width
        });

        layer.add(userImage);
        layer.batchDraw();

        var patternImage = new Konva.Image({
            width: 200,
            opacity: 0.5
        });

        var darthVaderGroup = new Konva.Group({
            x: 180,
            y: 50,
            draggable: true,
        });

        layer.add(darthVaderGroup);
        darthVaderGroup.add(patternImage);
        addAnchor(darthVaderGroup, 0, 0, 'topLeft');
        addAnchor(darthVaderGroup, 200, 0, 'topRight');
        addAnchor(darthVaderGroup, 200, 200, 'bottomRight');
        addAnchor(darthVaderGroup, 0, 200, 'bottomLeft');

        var imageObj_pattern = new Image();
        imageObj_pattern.onload = function () {
            patternImage.image(imageObj_pattern);
            layer.draw();
        };

        // change source
        imageObj_pattern.src = 'https://target.scene7.com/is/image/Target/GUEST_bd945555-f106-40e9-80ad-4c6668b4e534?wid=488&hei=488&fmt=pjpeg';
    };

    imageObj.src = imageSrc;
}

$(document).ready(function () {
    $(inputImage).change(function () {
        const input = this;

        $(imageFrame).empty();
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                var image = new Image();
                image.src = e.target.result;

                image.onload = function () {
                    drawCanvas(e.target.result, { width: this.width * 2, height: this.height * 2 }); // Fix Ratio
                }
            }

            reader.readAsDataURL(input.files[0]);

            $(processBtn).removeClass('d-none');
        }
    })
})