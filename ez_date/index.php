<?php
error_reporting(0);
highlight_file(__FILE__);
class date{
    public $a;
    public $b;
    public $file;
    public function __wakeup()
    {
        if(is_array($this->a)||is_array($this->b)){
            die('no array');
        }
        if( ($this->a !== $this->b) && (md5($this->a) === md5($this->b)) && (sha1($this->a)=== sha1($this->b)) ){
            $content=date($this->file);
            $uuid=uniqid().'.txt';
            file_put_contents($uuid,$content);
            $data=preg_replace('/((\s)*(\n)+(\s)*)/i','',file_get_contents($uuid));
            echo file_get_contents($data);
        }
        else{
            die();
        }
    }
}

unserialize(base64_decode($_GET['code']));