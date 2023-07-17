docker run -v /Users:/data --name RigidRegistration --rm ccts3.aws.chboston.org:5151/computationalradiology/crkit:latest /opt/crkit/bin/crlRigidRegistration

docker run -v home_local/daniellawson/Documents/projects/Warfieldatlas/subjects/ crkit:latest /opt/crkit/bin/crlRigidRegistration
* home_local/daniellawson/Documents/projects/Warfieldatlas/subjects/34613-042/session-8/fmri/1_3_12_2_1107_5_2_43_166200_2023040617472437272833536_0_0_0_dwi_acq... (not the right file)

docker run -v /home_local/daniellawson/Documents/projects/Registration/outputs:/data crkit:latest /opt/crkit/bin/crlRigidRegistration /data/RigidReg-bgpr6gym/volume_1.nii /data/RigidReg-bgpr6gym/volume_1.nii /data/RigidReg-bgpr6gym/testing.nii /data/RigidReg-bgpr6gym/transform_ouput.txt         