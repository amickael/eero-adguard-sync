FROM python:3.10-alpine
ENV PYTHONUNBUFFERED=1

ARG EAG_VERSION
RUN until pip install eero-adguard-sync==$EAG_VERSION; do sleep 1; done

COPY ./entrypoint.sh .
ENTRYPOINT ["./entrypoint.sh"]
CMD ["crond", "-f"]
