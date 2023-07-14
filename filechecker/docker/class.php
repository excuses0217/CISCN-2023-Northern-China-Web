<?php

class file
{
    public $name;
    public $data;
    public $ou;
    public function __wakeup()
    {
        // TODO: Implement __wakeup() method.
        $this->data='you need do something';
    }
    public function __call($name, $arguments)
    {
//        phpinfo();
        return $this->ou->b='78ty7badh2';
    }

    public function __destruct()
    {
        if (@file_get_contents($this->data) == "Hellociscccn") {
            $this->name->function();
        }


    }
}

class data
{
    public $a;
    public $oi;

    public function __set($name, $value)
    {
        // TODO: Implement __set() method.
        $this->yyyou();
        return "hhh";
    }

    public function yyyou()
    {
        system($this->oi);
    }
}