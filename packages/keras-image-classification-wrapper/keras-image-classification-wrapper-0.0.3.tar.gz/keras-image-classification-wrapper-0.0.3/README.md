# keras-image-classification-wrapper

A thin wrapper around keras image classification applications.

## Installation

```sh
pip install keras-image-classification-wrapper
```

## Usage

```python
def classify(
    image: Union[str, bytes, pillow.Image.Image],
    results: int = 3,
    model: str = INCEPTIONV3,
) -> tuple:
```

Classify an image.

`results` has to be less that 5, since keras applications don't give more than five results.

`model` has to be one of: `XCEPTION`, `VGG16`, `VGG19`, `RESNET50`, `RESNET101`, `RESNET152`, `RESNET50V2`, `RESNET101V2`, `RESNET152V2`, `RESNETRS101`, `RESNETRS152`, `RESNETRS200`, `RESNETRS270`, `RESNETRS350`, `RESNETRS420`, `REGNETX002`, `REGNETX004`, `REGNETX006`, `REGNETX008`, `REGNETX016`, `REGNETX032`, `REGNETX040`, `REGNETX064`, `REGNETX080`, `REGNETX120`, `REGNETX160`, `REGNETX320`, `REGNETY002`, `REGNETY004`, `REGNETY006`, `REGNETY008`, `REGNETY016`, `REGNETY032`, `REGNETY040`, `REGNETY064`, `REGNETY080`, `REGNETY120`, `REGNETY160`, `REGNETY320`, `INCEPTIONV3`, `INCEPTIONRESNETV2`, `MOBILENET`, `MOBILENETV2`, `MOBILENETV3SMALL`, `MOBILENETV3LARGE`, `DENSENET121`, `DENSENET169`, `DENSENET201`, `NASNETMOBILE`, `NASNETLARGE`, `EFFICIENTNETB0`, `EFFICIENTNETB1`, `EFFICIENTNETB2`, `EFFICIENTNETB3`, `EFFICIENTNETB4`, `EFFICIENTNETB5`, `EFFICIENTNETB6`, `EFFICIENTNETB7`, `EFFICIENTNETV2B0`, `EFFICIENTNETV2B1`, `EFFICIENTNETV2B2`, `EFFICIENTNETV2B3`, `EFFICIENTNETV2S`, `EFFICIENTNETV2M`, `EFFICIENTNETV2L`. Take a look at [model characteristics](https://keras.io/api/applications/#available-models), if you are not sure, which one to choose.

```python
def load_model(model: str) -> None:
```

Preload a model.

Loading of desired model is done automatically at the first call of `classify`. But it can take significant time, if weights need to be downloaded. So you can preload a model.

## Usage examples

With local files:

```python
import keras_image_classification as image_classification

file_path = "path/to/image.png"

labels = image_classification.classify(file_path, results = 3,
                                       model = image_classification.INCEPTIONV3)
print(labels)
```

With byte-like objects (here with [requests](https://pypi.org/project/requests/)):

```python
import requests
import keras_image_classification as image_classification

response = requests.get("https://http.cat/100")
assert response.status_code == 200

labels = image_classification.classify(response.content, results = 3,
                                       model = image_classification.INCEPTIONV3)
print(labels)
```

You can also pass [pillow](https://pypi.org/project/Pillow/) images directly:

```python
import PIL as pillow
import keras_image_classification as image_classification

file_path = "path/to/image.png"
image = pillow.Image.open(file_path)

labels = image_classification.classify(image, results = 3,
                                       model = image_classification.INCEPTIONV3)
print(labels)
```

Output:

```
({'imagenet_id': 'n02123394', 'label': 'Persian_cat', 'probability': 0.7993967533111572},
 {'imagenet_id': 'n06359193', 'label': 'web_site', 'probability': 0.03162319213151932},
 {'imagenet_id': 'n03598930', 'label': 'jigsaw_puzzle', 'probability': 0.013497020117938519})
```
