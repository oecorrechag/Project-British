import re

tecnología_y_software = ['software', 'enterprise software', 'saas', 'developer tools', 'open source', 'cloud computing', 'web development', 'project management', 'productivity', 'technology', 'paas', 'machine learning', 'hardware + software', 'hardware', 'electronics', 'automotive', 'internet', 'web hosting', 'file sharing', 'collaboration', 'messaging', 'synchronization', 'surveys',  'analytics', 'big data', 'predictive analytics', 'databases', 'web tools', 'information technology', 'development platforms', 'cloud infrastructure', 'virtualization', 'automation', 'wireless', 'testing', 'infrastructure', 'data integration', 'it management', 'devices', 'apps', 'android', 'cloud management', 'application performance monitoring app', 'presentations software', 'fraud detection', 'text analytics', 'knowledge management', 'mobility', 'data mining', 'seo', 'storage', 'document management', 'app stores', 'web browsers', 'webos', 'computers', 'web cms.', 'billing', 'quantitative marketing', 'optimization', 'forums', 'visualization', 'tools', 'navigation', 'facebook applications', 'google apps', 'personalization', 'cad hardware', 'nanotechnology', 'cloud data services', 'internet saas curated web', 'saas social media digital media', 'saas software news small and medium businesses advertising', 'voip', 'telephony', 'broadcasting', 'registrars', 'postal and courier services', 'retail software', 'geospatial', 'm2m', 'proximity', 'interface design', 'biometrics', 'task management', 'data', 'quantitative marketing', 'optimization', 'risk management', 'bioinformatics', 'geospatial', 'm2m', 'proximity', 'translation','enterprises', 'environmental innovation', 'archiving', 'energy', 'sustainability']
medios_y_entretenimiento = ['web design', 'graphics', 'image recognition', 'displays', 'usability', 'music', 'video', 'audio', 'media', 'content', 'internet radio market music', 'visual search', 'semantic search', 'news', 'reviews and recommendations', 'sports', 'games', 'design', 'user experience design', 'photography', 'photo sharing', 'meeting', 'search', 'digital media', 'streaming', 'fantasy sports', 'celebrity', 'publishing', 'concerts', 'ticketing', 'adventure', 'world domination', 'video games', 'entertainment', 'e-books', 'artists', 'broadcasting', 'saas social media digital media', 'interface design', 'visualization', 'printing', 'artists', 'web design', 'personalization', 'consumption', 'coffee', 'consumer internet', 'politics',]
comercio_y_negocios = ['e-commerce', 'marketplaces', 'shopping', 'commerce', 'consumer', 'gift card', 'auctions', 'fashion', 'curated web', 'startups', 'business', 'services', 'consulting', 'market research', 'lead generation', 'sales and marketing', 'marketing', 'advertising', 'public relations', 'crowdsourcing', 'freelancers', 'nonprofits', 'charity', 'small and medium businesses', 'subscription businesses', 'business services', 'consumer goods', 'mass customization', 'professional services', 'brand marketing', 'market', 'non profit', 'incubators', 'entrepreneur', 'customer service', 'management', 'outsourcing', 'b2b', 'ad targeting', 'coupons', 'groceries', 'retail', 'online shopping', 'flowers', 'pets', 'home renovation', 'employer benefits', 'quantitative marketing', 'stock exchanges', 'carbon', 'gambling', 'retail software', 'postal and courier services']
finanzas_y_seguros = ['credit cards', 'banking', 'trading', 'incentives', 'loyalty programs', 'finance', 'financial services', 'payments', 'bitcoin', 'health and insurance', 'insurance', 'billing', 'risk management', 'stock exchanges', 'carbon']
salud_y_bienestar = ['biotechnology', 'life sciences', 'health security', 'dental', 'fitness', 'baby boomers', 'families', 'parenting', 'health care', 'health and wellness', 'medical', 'health and insurance', 'hospitals', 'support', 'bioinformatics', 'doctors', 'physicians', 'health records', 'health care services', 'psychology', 'animal feed', 'clean energy', 'beauty', 'green']
educación_y_empleo = ['colleges', 'certification', 'professional services', 'entrepreneur', 'education', 'employment', 'recruiting', 'human resources', 'creative career', 'freelancers', 'teachers', 'employer benefits', 'management']
logística_y_transporte = ['cars', 'gps', 'sensors', 'construction', 'robotics', 'logistics', 'transportation', 'shipping', 'fleet management', 'supply chain', 'local', 'location based services', 'real time', 'tracking', 'manufacturing', 'postal and courier services', 'drones', 'aerospace', 'geospatial', 'navigation', 'printing', 'drones', 'aerospace', 'cad hardware', 'animal feed']
redes_sociales_y_comunicación = ['online dating', 'communications', 'microblogging', 'trusted networks', 'telecommunications', 'social media', 'social network', 'networking', 'social', 'chat', 'email', 'sms', 'peer-to-peer', 'twitter applications', 'blogging platforms', 'mobile', 'forums', 'facebook applications', 'google apps', 'telephony', 'voip', 'broadcasting', 'saas social media digital media']
bienes_raíces_legal_y_hospitalidad = ['legal', 'security', 'e-discovery', 'real estate', 'online rental', 'home & garden', 'restaurants', 'weddings', 'tourism', 'law enforcement', 'identity', 'health security', 'trusted networks', 'home renovation', 'hospitals', 'privacy', 'risk management', 'biometrics']
eventos_y_viajes = ['events', 'travel', 'hospitality', 'hotels', 'online reservations', 'event management',]


# Diccionario de mapeo de categorías
categorias_mapeo = {
    'tecnología_y_software': tecnología_y_software,
    'medios_y_entretenimiento': medios_y_entretenimiento,
    'comercio_y_negocios': comercio_y_negocios,
    'finanzas_y_seguros': finanzas_y_seguros,
    'salud_y_bienestar': salud_y_bienestar,
    'educación_y_empleo': educación_y_empleo,
    'logística_y_transporte': logística_y_transporte,
    'redes_sociales_y_comunicación': redes_sociales_y_comunicación,
    'bienes_raíces_legal_y_hospitalidad': bienes_raíces_legal_y_hospitalidad,
    'eventos_y_viajes': eventos_y_viajes
}

def amount(text):
    # Elimina caracteres no numéricos y divide en palabras
    words = str(text).split()
    
    # Filtra y limpia las palabras, convirtiéndolas en enteros
    numbers = [int(re.sub(r'\D', '', word)) for word in words if re.sub(r'\D', '', word).strip()]
    
    # Calcula la suma de los números
    total_sum = sum(numbers)
    
    # Obtiene el primer valor de la lista, o 0 si la lista está vacía
    first_value = numbers[0] if numbers else 0
    
    # Encuentra el primer valor diferente a 0
    first_non_zero = next((num for num in numbers if num != 0), 0)

    # Número de amounts
    len_number = len(numbers)
    
    # Retorna la suma, el primer valor y el primer valor diferente a 0
    return total_sum, first_value, first_non_zero, len_number
