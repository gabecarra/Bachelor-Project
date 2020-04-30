clear;
data = load('dataset_original.mat');
category = data.RELEASE.act;
file = data.RELEASE.annolist;
SIZE = size(data.RELEASE.act,1);

images = {};

for i = 1 : SIZE
    images(i).name = file(i).image.name;
    images(i).cat_name = category(i).cat_name;
    images(i).act_name = category(i).act_name;
    images(i).act_id = category(i).act_id;
end


save dataset_info images
