import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

i = 0


class ImageSubscriber(Node):
    def __init__(self):
        super().__init__("image_subscriber")
        self.subscription = self.create_subscription(
            # Image, "/color/video/image", self.image_callback, 10
            Image,
            # "/oak/rgb/image_raw",
            "/color/image",
            self.image_callback,
            10,
        )
        self.subscription  # prevent unused variable warning
        self.bridge = CvBridge()

    def image_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        Img_height, Img_width, _ = cv_image.shape
        title = f"Image Width: {Img_width} Image Height: {Img_height} {str(i)}"
        cv2.imshow(title, cv_image)
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    image_subscriber = ImageSubscriber()
    rclpy.spin(image_subscriber)
    image_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
