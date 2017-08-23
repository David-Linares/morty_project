-- Crear ambiente virtual
python3 -m venv asemienv

-- Instalar Django
pip3 install django

-- Copiar el proyecto

-- Instalar Devel tools
dnf install mariadb-devel

dnf install redhat-rpm-config

yum install python-devel
yum install python3-devel
pip3 install mysqlclient
--CentOs7
yum install mariadb-devel

pip3 install gTTS
pip3 install pydub
rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm
yum install ffmpeg ffmpeg-devel -y
