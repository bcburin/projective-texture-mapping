import matplotlib.pyplot as plt
from numpy import array

from src.polygon import Polygon


class PointSelector:
    def __init__(self):
        self._click_count = 0
        self._chosen_points = []
        self._fig = None
        self._cid = None
        self._num_required = None

    def _reset(self):
        self.__init__()

    def _on_click(self, event):
        if self._click_count < self._num_required:
            self._chosen_points.append(array([event.xdata, event.ydata]))
            self._click_count += 1
        if self._click_count == self._num_required:
            self._fig.canvas.mpl_disconnect(self._cid)
            plt.close()

    def request_polygon_from(self, image_path: str, n: int) -> Polygon:
        # Load your image
        image = plt.imread(image_path)
        # Display the image
        self._fig, ax = plt.subplots()
        ax.imshow(image)
        plt.title('Click four points on the image')
        # Capture mouse clicks
        self._num_required = n
        self._cid = self._fig.canvas.mpl_connect('button_press_event', self._on_click)
        plt.show()
        # get polygon
        polygon = Polygon(points=self._chosen_points)
        self._reset()
        return polygon


if __name__ == '__main__':
    # Example usage:
    point_selector = PointSelector()
    p = point_selector.request_polygon_from('../statics/aula-raquel.jpeg', n=4)
    print(p.as_list())
