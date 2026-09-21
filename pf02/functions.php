<?php
add_action('wp_enqueue_scripts', function () {
    wp_enqueue_style('kou-maintenance-child', get_stylesheet_uri(), [], wp_get_theme()->get('Version'));
});
add_shortcode('portfolio_notice', function ($atts, $content = null) {
    $atts = shortcode_atts(['date' => '', 'title' => '更新情報'], $atts, 'portfolio_notice');
    $title = esc_html($atts['title']);
    $date = esc_html($atts['date']);
    $body = wp_kses_post(do_shortcode($content ?? ''));
    ob_start(); ?>
    <section class="portfolio-notice">
      <strong><?php echo $title; ?></strong>
      <?php if ($date !== '') : ?><div class="portfolio-notice__date"><?php echo $date; ?></div><?php endif; ?>
      <div><?php echo $body; ?></div>
    </section>
    <?php return ob_get_clean();
});