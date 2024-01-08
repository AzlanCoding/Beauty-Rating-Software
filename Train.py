import facial_keypoints_detecter as fkd
import torch
import matplotlib.pyplot as plt
## Original dataset:
# Defining the data tranform >>
data_transform = fkd.preprocessing.Compose( [ fkd.preprocessing.Rescale(250),
                                              fkd.preprocessing.RandomCrop(224),
                                              fkd.preprocessing.Normalize(),
                                              fkd.preprocessing.ToTensor() ] )

# Applying transforms >>
dataset_train_original = fkd.data.FacialKeypointsDataset( csv_file  = 'C:/Users/azlan/AppData/Local/Programs/Python/Python310/Lib/site-packages/facial_keypoints_detecter/data/training_frames_keypoints.csv',
                                                          root_dir  = 'C:/Users/azlan/AppData/Local/Programs/Python/Python310/Lib/site-packages/facial_keypoints_detecter/data/training/',
                                                          transform = data_transform )

## Augmented dataset:
# Defining the data tranform >>
data_transform_rotate_clockwise = fkd.preprocessing.Compose( [fkd.preprocessing.Rescale(250),
                                                              fkd.preprocessing.RandomCrop(224),
                                                              fkd.preprocessing.Normalize(),
                                                              fkd.preprocessing.Rotate(-10),
                                                              fkd.preprocessing.Rescale(224),
                                                              fkd.preprocessing.ToTensor()] )

# Applying clockwise-rotation transform >>
dataset_rotate_clockwise = fkd.data.FacialKeypointsDataset( csv_file  = 'C:/Users/azlan/AppData/Local/Programs/Python/Python310/Lib/site-packages/facial_keypoints_detecter/data/training_frames_keypoints.csv',
                                                             root_dir  = 'C:/Users/azlan/AppData/Local/Programs/Python/Python310/Lib/site-packages/facial_keypoints_detecter/data/training/',
                                                             transform = data_transform_rotate_clockwise )

# Defining the data tranform >>
data_transform_rotate_anti_clockwise = fkd.preprocessing.Compose(  [fkd.preprocessing.Rescale(250),
                                                                    fkd.preprocessing.RandomCrop(224),
                                                                    fkd.preprocessing.Normalize(),
                                                                    fkd.preprocessing.Rotate(10),
                                                                    fkd.preprocessing.Rescale(224),
                                                                    fkd.preprocessing.ToTensor()] )

# Applying anti-clockwise-rotation transform >>
dataset_rotate_anti_clockwise = fkd.data.FacialKeypointsDataset( csv_file  = 'C:/Users/azlan/AppData/Local/Programs/Python/Python310/Lib/site-packages/facial_keypoints_detecter/data/training_frames_keypoints.csv',
                                                                 root_dir  = 'C:/Users/azlan/AppData/Local/Programs/Python/Python310/Lib/site-packages/facial_keypoints_detecter/data/training/',
                                                                 transform = data_transform_rotate_anti_clockwise )
# Combining original and augmented datasets >>
dataset_train = fkd.data.ConcatDataset( [ dataset_train_original,
                                          dataset_rotate_clockwise,
                                          dataset_rotate_anti_clockwise ])

# Printing some stats about the dataset >>
print('Number of images: ', len(dataset_train))

# Iterating through the transformed dataset and print some stats about the first few samples >>
for i in range(4):
    sample = dataset_train[i]
    print(i, sample['image'].size(), sample['keypoints'].size())

# load training data in batches
batch_size   = 10
train_loader = fkd.data.DataLoader( dataset_train, 
                                    batch_size  = batch_size,
                                    shuffle     = True, 
                                    num_workers = 0 )

# # loading in the test data >>
# dataset_test = fkd.data.datasets.test.combined

# Defining the data tranform >>
data_transform = fkd.preprocessing.Compose( [ fkd.preprocessing.Rescale(250),
                                              fkd.preprocessing.RandomCrop(224),
                                              fkd.preprocessing.Normalize(),
                                              fkd.preprocessing.ToTensor() ] )

# Applying transforms >>
dataset_test = fkd.data.FacialKeypointsDataset( csv_file  = 'C:/Users/azlan/AppData/Local/Programs/Python/Python310/Lib/site-packages/facial_keypoints_detecter/data/test_frames_keypoints.csv',
                                                root_dir  = 'C:/Users/azlan/AppData/Local/Programs/Python/Python310/Lib/site-packages/facial_keypoints_detecter/data/test/',
                                                transform = data_transform )

# load test data in batches >>
batch_size  = 10
test_loader =  fkd.data.DataLoader( dataset_test, 
                                    batch_size  = batch_size,
                                    shuffle     = True, 
                                    num_workers = 0 )
# Create an instance of class Net provided in the package >>
net = fkd.model.Net()
print(net)

# Running model on test sample input >>
# returns: test images, test predicted keypoints, test ground truth keypoints
test_images, test_outputs, gt_pts = net.sample_output(test_loader)

# print out the dimensions of the data to see if they make sense
print(test_images.data.size())
print(test_outputs.data.size())
print(gt_pts.size())
print("1")

fkd.plots.plot_output(test_images, test_outputs, gt_pts, batch_size = 10)

net.spec.dataset_train = dataset_train             
net.spec.batch_size    = 64                        # Batch size
net.spec.shuffle       = True                      # Shuffle training data
net.spec.num_workers   = 4                         # No. of cpu processors to use
net.spec.criterion     = torch.nn.SmoothL1Loss     # Loss function
net.spec.optimizer     = torch.optim.Adam          # Optimize
net.spec.learning_rate = 0.0005                    # Learning rate
net.spec.n_epochs      = 50                        # No. of epochs
print("2")
# # Calling `net.train_model` >>
list_loss = net.train_model()
print("3")

plt.xlabel("Epochs")
plt.ylabel(net.spec.criterion.__name__)
plt.plot( range(1,len(list_loss)+1), list_loss, "g-" )
print("4")
# Saving model parameters in file 'saved_models' >>
model_name = 'saved_model_facial_keypoints_detector.pt'
net.save_model(model_name)

net.load_model('saved_model_facial_keypoints_detector.pt')

# Running model on test sample input >>
test_images, test_outputs, gt_pts = net.sample_output(test_loader)

print(test_images.data.size())
print(test_outputs.data.size())
print(gt_pts.size())

# Visualizing test output >>
fkd.plots.plot_output(test_images, test_outputs, gt_pts)
