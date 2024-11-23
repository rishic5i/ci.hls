import logging
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class FieldExtractor:
    @staticmethod
    def extract_field(response, selector_dict, field_name, base_url=None):
        """Extract field value based on field type"""
        field_value = None
        try:
            if field_name in selector_dict:
                # Fields that should use .get()
                if field_name in ['title', 'article_date', 'attachment', 'contact_details']:
                    value = response.xpath(selector_dict[field_name]).get()
                    if value:
                        field_value = value.strip()
                        # Special handling for attachment URLs
                        if field_name == 'attachment' and base_url:
                            field_value = urljoin(base_url, field_value)

                # Fields that should use .getall() and join
                elif field_name in ['content', 'author']:
                    values = response.xpath(selector_dict[field_name]).getall()
                    if values:
                        field_value = ' '.join(values).replace('\n', '').replace('\t', '').strip()

                # Special handling for published_date - take last element
                elif field_name == 'published_date':
                    values = response.xpath(selector_dict[field_name]).getall()
                    if values:
                        try:
                            field_value = values[-1].replace('\n', '').replace('\t', '').strip()
                        except:
                            field_value = values

                # Default to .get() for any other fields
                else:
                    value = response.xpath(selector_dict[field_name]).get()
                    if value:
                        field_value = value.strip()

        except Exception as e:
            logger.warning(f"Error extracting {field_name}: {e}")

        return field_value
