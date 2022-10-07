import pytest
import helper
import numpy as np

class Test_GetColorChannel:
	def test_grayscale_channel(self):
		# Define a "phony" cv.Mat classe that we can use to imitate how a grayscale image reports it's shape
		class grayscale_img:
			shape = (128,128)
		assert helper.getColorChannels(grayscale_img) == 1

	@pytest.mark.parametrize("i", [*range(1, 4)])
	def test_3_color_channels(self, i):
		# Define a "phony" cv.Mat class that we can use to imitate how a 3-channel color image reports it's shape
		class color_img:
			shape = [128,128,i]
		# Check that we actually get 1,2 and 3 returned to us
		assert helper.getColorChannels(color_img) == i

	def test_invalid_channels(self):
		class too_few_shape:
			shape = [128]
		# Check that a shape with only 1 item gives off an error
		with pytest.raises(ValueError):
			helper.getColorChannels(too_few_shape)

		class too_many_shape:
			shape = [123,123,123,123]
		# Check that a shape with 4 items gives off a ValueError
		with pytest.raises(ValueError):
			helper.getColorChannels(too_many_shape)

class Test_masker:
	def test_masking_rectangle_mask(self):
		# Load a setup of the masker with a 4x4 pixel grayscale image
		temp_masker = helper.masker(np.zeros((4,4,1), dtype="uint8"))
		# Then mask a 2x2 section in the middle so it will be visible
		temp_masker.mask_rectangle((1,1),(2,2),True)

		# Create a pre-defined black image, and paint a white square in the middle
		predefined_image = np.zeros((4,4,1), dtype="uint8")
		predefined_image[1][1][0] = 255
		predefined_image[1][2][0] = 255
		predefined_image[2][1][0] = 255
		predefined_image[2][2][0] = 255

		# Compare the masking image from the masker, and the pre-defined image we defined above.
		assert np.array_equal(temp_masker.mask, predefined_image)
	
	def test_masking_rgb_image(self):
		# Make sure that the masker class will object to the treatement of getting a color image
		# when it needs to be a grayscale image
		with pytest.raises(ValueError):
			helper.masker(np.zeros((4,4,3), dtype="uint8")) # Generate a 4x4 image, with BGR color spacing, which is not grayscale
	
	def test_center_x(self):
		# Check if the calculation for the X-axis centerpoint really is correct on a 6x6 black grayscale image.
		tmp_masker = helper.masker(np.zeros((6,6,1), dtype="uint8"))
		assert tmp_masker.x_center == 3
	
	def test_center_y(self):
		# Check if the calculation for the Y-axis centerpoint really is correct on a 6x6 black grayscale image.
		tmp_masker = helper.masker(np.zeros((6,6,1), dtype="uint8"))
		assert tmp_masker.y_center == 3
	
	def test_get_image_even_number(self):
		# Check if the function will throw a ValueError incase the given number is even.
		tmp_masker = helper.masker(np.zeros((10,10,1), dtype="uint8"))
		with pytest.raises(ValueError):
			tmp_masker.get_image(2) # This should throw an error
		assert tmp_masker.get_image(3).all() != None # This shouldn't throw a error, but shouldn't return nothing