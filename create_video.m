%%%%%%%%%%%%%%%%%%%%%%%%%%
% Create a video

% Directories
workingDir = 'C:\klemen\Repositories\ProCyclingStats\Analysis_Tables\PCS_pts_vs_Velogames_score\PCS_Overall_correlation\';


imageNames = dir(fullfile(workingDir,'*.png'));
imageNames = {imageNames.name}';




outputVideo = VideoWriter(fullfile(workingDir,'PCS_Overall.avi'));
outputVideo.FrameRate = 1;
open(outputVideo)

for ii = 1:length(imageNames)
   img = imread(fullfile(workingDir,imageNames{ii}));
   writeVideo(outputVideo,img)
end


close(outputVideo)
