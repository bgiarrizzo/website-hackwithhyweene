# -----------------------------------------------------------------------------
# Build Image

ARG SWIFT_VERSION=6.3
ARG DEBIAN_VERSION=bookworm
ARG IMAGE_SIZE=slim

FROM swift:${SWIFT_VERSION}-${DEBIAN_VERSION}-${IMAGE_SIZE} AS builder

WORKDIR /app

COPY . /app/

RUN cd src && \
    swift package resolve && \
    swift build -c release && \
    cd .. && \
    ./src/.build/release/hyweene build --docker

# -----------------------------------------------------------------------------
# Final image

FROM nginx:alpine AS final

COPY --from=builder /app/current/ /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]