%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Png merge using ImageMagick
% 
% by Klemen Ziberna
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clear;
close all;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% GLOBAL VARIABLES
INPUT_FOLDER = 'C:\klemen\Repositories\ProCyclingStats\Analysis_Tables\PCS_pts_vs_Velogames_score\PCS_Season_correlation\';
OUTPUT_FOLDER = 'C:\klemen\Repositories\ProCyclingStats\Analysis_Tables\PCS_pts_vs_Velogames_score\PCS_Season_correlation\';
fileName = 'PCS_Season_correlation';
%start_ind = [01];
%end_ind = [14];

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Create a list with all the files to be merged
%all_ind = start_ind : end_ind;

% for i = 1:numel(all_ind)
%     all_image_files{i} = ...
%         [INPUT_FOLDER, num2str(all_ind(i)), '.png'];
% end

imageNames = dir(fullfile(INPUT_FOLDER,'*.png'));
%imageNames = {imageNames.name}';

all_image_files = {}
for i = 1:length(imageNames)
    all_image_files{i} = ...
        [INPUT_FOLDER, imageNames(i).name];
    
end



% Create a string with all the files
all_images_string = strjoin(all_image_files);

% Create a command string
% montage_string = ...
%     ['montage ', all_images_string, ...
%     '-geometry 375x250+4+3 -tile 7x3 "', fileName, ...
%     '" ', OUTPUT_FOLDER, fileName, '.png'];

montage_string2 = ...
    ['montage ', all_images_string, ...
    ' -mode Concatenate -title "PCS Season Points" ', ...
    OUTPUT_FOLDER, fileName, '.png'];


% Run the system command
command = montage_string2;
[status, cmdout] = system(command);


