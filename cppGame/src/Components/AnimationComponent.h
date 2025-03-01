#ifndef ANIMATIONCOMPONENT_H
#define ANIMATIONCOMPONENT_H

#include <map>
#include <iostream>
#include <string>

#include <SFML/System.hpp>
#include <SFML/Window.hpp>
#include <SFML/Graphics.hpp>
#include <SFML/Audio.hpp>
#include <SFML/Network.hpp>

class AnimationComponent
{
    private:

        class Animation
        {
            public:
                // Variables
                sf::Sprite& sprite;
                sf::Texture& textureSheet;
                float animationTimer;
                float timer;
                bool done;
                int width;
                int height;
                sf::IntRect startRect;
                sf::IntRect currentRect;
                sf::IntRect endRect;

                Animation(sf::Sprite& sprite, sf::Texture& texture_sheet,
                    float animation_timer,
                    int start_frame_x, int start_frame_y, int frames_x, int frames_y, int width, int height)
                    : sprite(sprite), textureSheet(texture_sheet),
                    animationTimer(animation_timer), timer(0.f), done(false),
                    width(width), height(height)
                {
                    this->timer = 0.f;
                    this->startRect = sf::IntRect(start_frame_x * width, start_frame_y * height, width, height);
                    this->currentRect = this->startRect;
                    this->endRect = sf::IntRect(frames_x * width, frames_y * height , width, height);

                    this->sprite.setTexture(this->textureSheet, true);
                    this->sprite.setTextureRect(this->startRect);
                }

            // Functions

            bool play(const float& dt)
            {
                // Update timer
                bool done = false;
                this->timer += 100.f * dt;
                if(this->timer >= this->animationTimer)
                {
                    // Reset timer
                    this->timer = 0.f;

                    // Animate
                    if(this->currentRect != this->endRect)
                    {
                        this->currentRect.left += this->width;
                    }
                    else  // Reset
                    {
                        this->currentRect.left = this->startRect.left;
                        done = true;
                    }

                    this->sprite.setTextureRect(this->currentRect);
                }

                return done;
            }


            bool play(const float& dt, float mod_percent)
            {
                // Update timer
                bool done = false;
                if(mod_percent < 0.5f)
                {
                    mod_percent = 0.5f;
                }
                
                bool done = false;
                this->timer += mod_percent * 100.f * dt;
                if(this->timer >= this->animationTimer)
                {
                    // Reset timer
                    this->timer = 0.f;

                    // Animate
                    if(this->currentRect != this->endRect)
                    {
                        this->currentRect.left += this->width;
                    }
                    else  // Reset
                    {
                        this->currentRect.left = this->startRect.left;
                        done = true;
                    }

                    this->sprite.setTextureRect(this->currentRect);
                }

                return done;
            }

            void reset()
            {
                this->timer = this->animationTimer;
                this->currentRect = this->startRect;
            }
        };

        sf::Sprite& sprite;
        sf::Texture& textureSheet;
        std::map<std::string, Animation*> animations;
        Animation* lastAnimation;
        Animation* priorityAnimation;


    public:
        AnimationComponent(sf::Sprite& sprite, sf::Texture& texture_sheet);
        virtual ~AnimationComponent();


        // Functions
        void addAnimation(const std::string key,
            float animation_timer,
            int start_frame_x, int start_frame_y, int frames_x, int frames_y, int width, int height);

        void play(const std::string key, const float& dt, const bool priority = false);
        void play(const std::string key, const float& dt, const float& modifier, const float& modifier_max, const bool priority = false);


};

#endif