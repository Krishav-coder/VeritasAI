import cv2
import numpy as np
import tensorflow as tf

IMG_SIZE = (299, 299)
LAST_CONV_LAYER = "block12_sepconv2_act"


def preprocess_image(image_path):
    """
    Returns:
        img_tensor : (1,299,299,3)
        img_orig   : RGB uint8 image
    """

    img = cv2.imread(image_path)

    if img is None:
        raise ValueError(f"Could not load image: {image_path}")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img_orig = cv2.resize(img, IMG_SIZE)

    img_tensor = tf.keras.applications.xception.preprocess_input(
        img_orig.astype(np.float32)
    )

    img_tensor = np.expand_dims(img_tensor, axis=0)

    return img_tensor, img_orig


def find_last_conv_layer(model, requested):

    try:
        model.get_layer(requested)
        return model, requested
    except ValueError:
        pass

    xception = model.layers[0]

    try:
        xception.get_layer(requested)
        return xception, requested
    except ValueError:
        pass

    conv_candidates = [
        layer.name
        for layer in xception.layers
        if isinstance(
            layer,
            (
                tf.keras.layers.Conv2D,
                tf.keras.layers.SeparableConv2D,
                tf.keras.layers.DepthwiseConv2D,
                tf.keras.layers.Activation,
            ),
        )
        and hasattr(layer, "output_shape")
        and len(layer.output_shape) == 4
    ]

    if not conv_candidates:
        raise RuntimeError("No convolution layer found.")

    return xception, conv_candidates[-1]


def compute_gradcam(model, img_tensor, last_conv_layer=LAST_CONV_LAYER):

    grad_model_src, layer_name = find_last_conv_layer(
        model,
        last_conv_layer,
    )

    conv_layer = grad_model_src.get_layer(layer_name)

    grad_model = tf.keras.Model(
        inputs=grad_model_src.input,
        outputs=[
            conv_layer.output,
            grad_model_src.output,
        ],
    )

    use_full_model = grad_model_src is not model

    with tf.GradientTape() as tape:

        img_tensor = tf.cast(img_tensor, tf.float32)

        if use_full_model:

            conv_output, sub_output = grad_model(
                img_tensor,
                training=False,
            )

            x = sub_output

            for layer in model.layers[1:]:
                x = layer(x, training=False)

            prediction = x

        else:

            conv_output, prediction = grad_model(
                img_tensor,
                training=False,
            )

        class_channel = prediction[:, 0]

    grads = tape.gradient(class_channel, conv_output)

    if grads is None:
        raise RuntimeError("Gradients are None.")

    pooled_grads = tf.reduce_mean(
        grads,
        axis=(0, 1, 2),
    )

    conv_output = conv_output[0]

    heatmap = conv_output @ pooled_grads[..., tf.newaxis]

    heatmap = tf.squeeze(heatmap)

    heatmap = tf.maximum(heatmap, 0)

    heatmap /= tf.reduce_max(heatmap) + 1e-8

    heatmap = heatmap.numpy()

    probability = float(prediction[0][0])

    return heatmap, probability


def overlay_heatmap(
    heatmap,
    original_image,
    alpha=0.45,
):

    h, w = original_image.shape[:2]

    heatmap = np.uint8(255 * heatmap)

    heatmap = cv2.resize(
        heatmap,
        (w, h),
    )

    heatmap = cv2.applyColorMap(
        heatmap,
        cv2.COLORMAP_JET,
    )

    heatmap = cv2.cvtColor(
        heatmap,
        cv2.COLOR_BGR2RGB,
    )

    overlay = cv2.addWeighted(
        original_image,
        1 - alpha,
        heatmap,
        alpha,
        0,
    )

    return overlay