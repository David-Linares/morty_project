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
yum install python36u-mod_wsgi


--PDFKIT

wget http://download.gna.org/wkhtmltopdf/0.12/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
unxz wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
tar -xvf wkhtmltox-0.12.4_linux-generic-amd64.tar
mv wkhtmltox/bin/* /usr/local/bin/
rm -rf wkhtmltox
rm -f wkhtmltox-0.12.4_linux-generic-amd64.tar

--JWT
pip3 install PyJWT
pip3 install imgkit



--

- Trigonométricas (sin, cos, tan, cot, csc, sec, ln, log, infty)
- Letras griegas Minúscula (Pi, Theta, Deltha, Omega, Mu, Lambda)
- Binarios (Cap, Cop)
- Relación (leq, geq)
- Flechas (rightarrow, longrightarrow)
- Varios (Forall, exists, neg, nexists)
- Tamaño variable (Sum, int, oint, )
- Otras construcción (sqrt, sqrt[n], frac)
- matrices(binom, matrix, )