FROM raspbian/stretch:latest as BASE
MAINTAINER rustem.dautov@sintef.no

RUN apt-get update && apt-get install -y \
  libmosquitto-dev \
#  libbluetooth-dev \
#  libconfuse-dev \
#  libffi-dev \
#  libssl-dev \
  build-essential \
#  avrdude \
#  python-pip \
#  python-setuptools \
#  libgps-dev \
#  gpsd \
#  gpsd-clients \
#  wiringpi \
  libmicrohttpd-dev

COPY ./ansible/public-files/gateway.conf /etc/tellugw/
COPY ./ansible/public-files/scripts/* /etc/tellugw/scripts/
ADD ./ansible/releases/enact-1.2.tar.gz /etc/tellugw/
WORKDIR /etc/tellugw/enact-1.2/Prometheus/
RUN make
CMD ["/etc/tellugw/enact-1.2/Prometheus/Prometheus"]
#CMD ["/etc/tellugw/enact-1.2/NetworkAgent/NetworkAgent"]
