<div>
    <form action="file.php" method="post" enctype="multipart/form-data">
        <label for="file">filename:</label>
        <input type="file" name="file" id="file"><br>
        <input type="submit" name="submit" value="submit">
</div>
<?php
include "file.php";
include "class.php";
echo "goto filecheck.php";
$filepath=$_POST['filepath'];
if(preg_match('/^(ftp|zlib|data|glob|phar|ssh2|compress.bzip2|compress.zlib|rar|ogg|expect)(.|\\s)*|(.|\\s)*(file|data|\.\.)(.|\\s)*/i',$filepath)){
    echo "<br>";
    die("Don't give me dangerous code");
}
else
{
if(empty($filepath)){
    die();
}
else{
    $mime= mime_content_type($filepath);
    echo "Image format is".$mime;
}
}
