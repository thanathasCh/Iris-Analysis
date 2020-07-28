let inputImage = '#input-image';
let imageFrame = '#image-frame';


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


function drawCanvas() {
    var width = window.innerWidth;
    var height = window.innerHeight;

    var stage = new Konva.Stage({
        container: 'image-frame',
        width: width,
        height: height,
    });

    var layer = new Konva.Layer();
    stage.add(layer);

    // darth vader
    var darthVaderImg = new Konva.Image({
        width: 200,
        height: 137,
        opacity: 0.5
    });

    // yoda
    var yodaImg = new Konva.Image({
        width: 93,
        height: 104,
        opacity: 0.5
    });

    var darthVaderGroup = new Konva.Group({
        x: 180,
        y: 50,
        draggable: true,
    });
    layer.add(darthVaderGroup);
    darthVaderGroup.add(darthVaderImg);
    addAnchor(darthVaderGroup, 0, 0, 'topLeft');
    addAnchor(darthVaderGroup, 200, 0, 'topRight');
    addAnchor(darthVaderGroup, 200, 138, 'bottomRight');
    addAnchor(darthVaderGroup, 0, 138, 'bottomLeft');

    var yodaGroup = new Konva.Group({
        x: 20,
        y: 110,
        draggable: true,
    });
    layer.add(yodaGroup);
    yodaGroup.add(yodaImg);
    addAnchor(yodaGroup, 0, 0, 'topLeft');
    addAnchor(yodaGroup, 93, 0, 'topRight');
    addAnchor(yodaGroup, 93, 104, 'bottomRight');
    addAnchor(yodaGroup, 0, 104, 'bottomLeft');

    var imageObj1 = new Image();
    imageObj1.onload = function () {
        darthVaderImg.image(imageObj1);
        layer.draw();
    };
    imageObj1.src = 'https://target.scene7.com/is/image/Target/GUEST_bd945555-f106-40e9-80ad-4c6668b4e534?wid=488&hei=488&fmt=pjpeg';

    var imageObj2 = new Image();
    imageObj2.onload = function () {
        yodaImg.image(imageObj2);
        layer.draw();
    };
    imageObj2.src = 'https://upload.wikimedia.org/wikipedia/en/9/9b/Yoda_Empire_Strikes_Back.png';
}

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

    drawCanvas();
})