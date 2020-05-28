docker build -t adv_dev_checker_image .
docker run --rm adv_dev_checker_image python /work/handler.py
