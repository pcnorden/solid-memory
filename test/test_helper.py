import pytest
import helper

def test_grayscale_channel():
	# Define a "phony" cv.Mat classe that we can use to imitate how a grayscale image reports it's shape
	class grayscale_img:
		shape = (128,128)
	assert helper.getColorChannels(grayscale_img) == 1

def test_3_channels():
	# Define a "phony" cv.Mat class that we can use to imitate how a 3-channel color image reports it's shape
	class color_img:
		shape = [128,128,1]
	item = color_img # Create a copy that we can modify between calls, with it telling us right now it only
	# has a single image channel
	assert helper.getColorChannels(item) == 1
	
	# Change the color space to have 2 color channels in the image somehow
	item.shape[2] = 2
	assert helper.getColorChannels(item) == 2
	# Change the color space to have 3 color channels in the image
	item.shape[2] = 3
	assert helper.getColorChannels(item) == 3
	
def test_invalid_channels():
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