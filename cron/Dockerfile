FROM alpine:3.13

RUN apk add logrotate

COPY ./logrotate-cron /etc/cron.d/
COPY ./logrotate.conf /etc/logrotate.d/
RUN chown root:root /etc/cron.d/logrotate-cron /etc/logrotate.d/logrotate.conf && \
    chmod 644 /etc/cron.d/logrotate-cron /etc/logrotate.d/logrotate.conf && \
    crontab /etc/cron.d/logrotate-cron

CMD ["crond", "-f", "-l", "8"]
