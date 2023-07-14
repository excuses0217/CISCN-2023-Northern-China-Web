<?php
function file_check() {
    global $_FILES;
    $allowed_types = array("jpg","gif","png");
    $temp = explode(".",$_FILES["file"]["name"]);
    $extension = end($temp);
    if(empty($extension)) {
        return  false;
    }
    else{
        if(in_array($extension,$allowed_types)) {
            return true;
        }
        else {
            echo 'Please upload images in jpg png gif format';
            return false;
        }
    }
}
function move_File() {
    global $_FILES;
    $filename = md5($_FILES["file"]["name"]).".jpg";
    if(file_exists("upload/" . $filename)) {
        unlink($filename);
    }
    move_uploaded_file($_FILES["file"]["tmp_name"],"upload/" . $filename);
    echo "upload sucess! image saved :upload/".$filename;
}
if(file_check()){
    move_File();
}