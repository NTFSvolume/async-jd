FROM jlesage/jdownloader-2

COPY ./org.jdownloader.api.RemoteAPIConfig.json /org.jdownloader.api.RemoteAPIConfig.json
COPY ./60-local-API-settings.sh /etc/cont-init.d/60-local-API-settings.sh
RUN chmod +x /etc/cont-init.d/60-local-API-settings.sh
